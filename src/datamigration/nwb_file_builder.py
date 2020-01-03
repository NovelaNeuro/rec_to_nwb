import logging
import os

from hdmf.common import VectorData, DynamicTable
from pynwb import NWBHDF5IO, NWBFile
from pynwb.ecephys import ElectrodeGroup

import src.datamigration.file_scanner as fs
from src.datamigration.extension.probe import Probe
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.header_checker.rec_file_finder import RecFileFinder
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor
from src.datamigration.nwb_builder.probe_extractor import ProbesExtractor
from src.datamigration.xml_extractor import XMLExtractor

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self, data_path, animal_name, date, metadata_path, probes_path, output_file='output.nwb'):
        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_folder = fs.DataScanner(data_path)
        self.dataset_names = self.data_folder.get_all_datasets(animal_name, date)
        self.datasets = [self.data_folder.data[animal_name][date][dataset_mda] for dataset_mda in self.dataset_names]

        self.output_file = output_file

        self.metadata = MetadataExtractor(config_path=metadata_path)
        self.probes_yml = ProbesExtractor(probes_path=probes_path)
        self.__check_headers_compatibility()
        self.spike_n_trodes = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                                     self.date + '/header.xml').configuration.spike_configuration.spike_n_trodes

    def build(self):

        content = NWBFile(session_description=self.metadata.session_description,
                          experimenter=self.metadata.experimenter_name,
                          lab=self.metadata.lab,
                          institution=self.metadata.institution,
                          session_start_time=self.metadata.session_start_time,
                          identifier=str(self.metadata.identifier),
                          experiment_description=self.metadata.experiment_description,
                          subject=self.metadata.subject,
                          )

        self.__build_task(content)

        self.__build_position(content)

        self.__build_apparatus(content)

        probes = self.__add_devices(content)

        groups = self.__add_electrode_group(content, probes)

        self.__add_electrodes(content, groups)

        # self.__build_dio(content)

        # self.__build_mda(content)

        return content

    def __check_headers_compatibility(self,):
        rec_files = RecFileFinder().find_rec_files(self.data_path + self.animal_name + '/raw')
        header_extractor = HeaderFilesExtractor()
        xml_files = header_extractor.extract(rec_files)
        header_reader = HeaderReader(xml_files)
        xml_headers = header_reader.read_headers()
        comparator = HeaderComparator(xml_headers)
        if not comparator.compare():
            message = 'Rec files: ' + str(rec_files) + ' contain incosistent xml headers!'
            differences = [diff for diff in header_reader.headers_differences
                           if not 'systemTimeAtCreation' in str(diff) and not 'timestampAtCreation'
                                                                              in str(diff)]
            logging.warning(message, differences,)
            with open('headers_comparission_log.log', 'w') as headers_log:
                headers_log.write(str(message + '\n'))
                headers_log.write(str(differences))

        XMLExtractor(rec_path=rec_files[0],
                     xml_path=self.data_path + '/' + self.animal_name + '/preprocessing/' +
                              self.date + '/header.xml').extract_xml_from_rec_file()

    def __create_region(self, content):
        region = content.create_electrode_table_region(
            description=self.metadata.electrode_regions[0]['description'],
            region=self.metadata.electrode_regions[0]['region'])
        return region

    def __add_electrodes(self, content, groups):
        rel_x = []
        rel_y = []
        rel_z = []
        for probe_file in self.probes_yml.probes_content:
            for shank in probe_file['shanks']:
                group = next((group for group in groups
                              if group.name == str(shank['electrode_group_name'])),
                             'Error, no corresponding electrode_group')
                location = group.location
                for electrode in shank['electrodes']:
                    content.add_electrode(
                        x=0.0,
                        y=0.0,
                        z=0.0,
                        imp=0.0,
                        location=location,
                        filtering='None',
                        group=group,
                        id=int(electrode['electrode'].split('probe_electrode_')[1]),
                    )
                    rel_x.append(electrode['rel_x'])
                    rel_y.append(electrode['rel_y'])
                    rel_z.append(electrode['rel_z'])

        content.electrodes.add_column(
            name='rel_x',
            description='rel_x sample description',
            data=rel_x
        )
        content.electrodes.add_column(
            name='rel_y',
            description='rel_y sample description',
            data=rel_y
        )
        content.electrodes.add_column(
            name='rel_z',
            description='rel_z sample description',
            data=rel_z
        )

    def __add_electrode_group(self, content, probes):
        groups = []
        for electrode_group_dict in self.metadata.electrode_groups:
            groups.append(
                ElectrodeGroup(
                    name=str(electrode_group_dict['name']),
                    description=electrode_group_dict['description'],
                    location=electrode_group_dict['location'],
                    device=[probe for probe in probes
                            if probe.name == electrode_group_dict['device']][0]
                )
            )
        for group in groups:
            content.add_electrode_group(group)
        return groups

    def __add_devices(self, content):
        probes = []
        for probe_dict in self.probes_yml.probes_content:
            probes.append(
                Probe(
                    name=probe_dict['probe_type'],
                    probe_description=probe_dict['probe_description'],
                    device_name=self.metadata.devices[0]
                )
            )
        for probe in probes:
            content.add_device(probe)
        return probes

    def __build_mda(self, content):
        sampling_rate = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                               self.date + '/header.xml').configuration.hardware_configuration.sampling_rate
        mda_extractor = MdaExtractor(self.datasets)
        electrode_table_region = self.__create_region(content)
        series = mda_extractor.get_mda(electrode_table_region, sampling_rate)
        content.add_acquisition(series)

    def __build_dio(self, content):
        extracted_dio = DioExtractor(data_path=self.data_path + '/' + self.animal_name + '/preprocessing/' + self.date,
                                     metadata=self.metadata)
        content.create_processing_module(
            name='behavioral_event',
            description=''
        ).add_data_interface(
            extracted_dio.get_dio()
        )

    def __build_apparatus(self, content):
        apparatus_columns = []
        for counter, row in enumerate(self.metadata.apparatus):
            apparatus_columns.append(VectorData(name='col ' + str(counter), description='', data=row))
        content.create_processing_module(
            name='apparatus',
            description='Sample description'
        ).add_data_interface(
            DynamicTable(
                name='apparatus',
                description='Sample description',
                id=None,
                columns=apparatus_columns
            )
        )

    def __build_position(self, content):
        pos_extractor = POSExtractor(self.datasets)
        content.create_processing_module(
            name='position',
            description='Sample description'
        ).add_data_interface(
            pos_extractor.get_position()
        )

    def __build_task(self, content):
        nwb_table = DynamicTable(
            name='task',
            description='Sample description',
        )

        nwb_table.add_column(
            name='task_name',
            description='Sample description',
        )
        nwb_table.add_column(
            name='task_description',
            description='Sample description',
        )
        for task in self.metadata.tasks:
            nwb_table.add_row(task)

        content.create_processing_module(
            name='task',
            description='Sample description'
        ).add_data_interface(nwb_table)

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
