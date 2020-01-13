import datetime
import logging
import os

from hdmf.common import VectorData, DynamicTable
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.file_scanner as fs
from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.ntrode import NTrode
from src.datamigration.extension.probe import Probe
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.header_checker.rec_file_finder import RecFileFinder
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor
from src.datamigration.xml_extractor import XMLExtractor

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self, data_path, animal_name, date, nwb_metadata, output_file='output.nwb'):
        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_folder = fs.DataScanner(data_path)
        self.dataset_names = self.data_folder.get_all_datasets(animal_name, date)
        self.datasets = [self.data_folder.data[animal_name][date][dataset_mda] for dataset_mda in self.dataset_names]

        self.output_file = output_file

        self.metadata = nwb_metadata.metadata.metadata
        self.probes = nwb_metadata.probes
        self.__check_headers_compatibility()
        self.spike_n_trodes = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                                     self.date + '/header.xml').configuration.spike_configuration.spike_n_trodes


    def build(self):
        content = NWBFile(session_description=self.metadata['session description'],
                          experimenter=self.metadata['experimenter name'],
                          lab=self.metadata['lab'],
                          institution=self.metadata['institution'],
                          session_start_time=datetime.datetime.strptime(
                              self.metadata['session start time'], '%m/%d/%Y %H:%M:%S'
                          ),
                          identifier=str(self.metadata['identifier']),
                          experiment_description=self.metadata['experiment description'],
                          subject=Subject(
                              description=self.metadata['subject']['description'],
                              genotype=self.metadata['subject']['genotype'],
                              sex=self.metadata['subject']['sex'],
                              species=self.metadata['subject']['species'],
                              subject_id=self.metadata['subject']['subject id'],
                              weight=str(self.metadata['subject']['weight']),
                          ),
                          )

        self.__build_task(content)

        self.__build_position(content)

        self.__build_aparatus(content)

        probes = self.__add_devices(content)

        self.__build_electrode_groups(content, probes)

        self.__build_ntrodes(content, probes)

        #self.__add_electrodes(content)

        self.__build_dio(content)

       # self.__add_electrodes_extensions(content, self.spike_n_trodes)

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
                           if 'systemTimeAtCreation' not in str(diff) and 'timestampAtCreation'
                           not in str(diff)]
            logging.warning(message, differences,)
            with open('headers_comparission_log.log', 'w') as headers_log:
                headers_log.write(str(message + '\n'))
                headers_log.write(str(differences))

        XMLExtractor(rec_path=rec_files[0],
                     xml_path=self.data_path + '/' + self.animal_name + '/preprocessing/' +
                              self.date + '/header.xml').extract_xml_from_rec_file()

    def __create_region(self, content):
        region = content.create_electrode_table_region(
            description=self.metadata['electrode region']['description'],
            region=self.metadata['electrode region']['region'],
            name=self.metadata['electrode region']['name']
        )
        return region

    @staticmethod
    def __add_electrodes_extensions(content, spike_n_trodes):
        maxDisp = []
        triggerOn = []
        hwChan = []
        thresh = []
        for trode in spike_n_trodes:
            for channel in trode.spike_channels:
                maxDisp.append(channel.max_disp)
                triggerOn.append(channel.trigger_on)
                hwChan.append(channel.hw_chan)
                thresh.append(channel.thresh)
        content.electrodes.add_column(
            name='maxDisp',
            description='maxDisp sample description',
            data=maxDisp
        )
        content.electrodes.add_column(
            name='thresh',
            description='thresh sample description',
            data=thresh
        )
        content.electrodes.add_column(
            name='hwChan',
            description='hwChan sample description',
            data=hwChan
        )
        content.electrodes.add_column(
            name='triggerOn',
            description='triggerOn sample description',
            data=triggerOn
        )

    def __add_electrodes(self, content):
        for electrode in self.metadata.electrodes:
            content.add_electrode(
                x=electrode['x'],
                y=electrode['y'],
                z=electrode['z'],
                imp=1.0,
                location='necessary location',
                filtering=electrode['filtering'],
                group=content.electrode_groups['1'],
                id=electrode['id'],
            )

    def __build_electrode_groups(self, content, probes):
        fl_groups = []
        for electrode_group_metadata in self.metadata['electrode groups']:
            group = self.__create_electrode_group(electrode_group_metadata, probes)
            fl_groups.append(group)
        for fl_group in fl_groups:
            content.add_electrode_group(fl_group)

    @staticmethod
    def __create_electrode_group(metadata, probes):
        for probe in probes:
            if probe.name == str(metadata["probe_id"]):
                device = probe
                break
        electrode_group = FLElectrodeGroup(
            probe_id=metadata["probe_id"],
            id=metadata['id'],
            device=device,
            location=str(metadata['location']),
            description=str(metadata['description']),
            name='electrode group ' + str(metadata["id"])
        )
        return electrode_group

    def __build_ntrodes(self, content, probes):
        fl_ntrodes = []
        for ntrode_metadata in self.metadata['ntrode probe channel map']:
            fl_ntrode = self.__create_ntrode(ntrode_metadata, probes)
            fl_ntrodes.append(fl_ntrode)
        for fl_ntrode in fl_ntrodes:
            content.add_electrode_group(fl_ntrode)

    @staticmethod
    def __create_ntrode(metadata, probes):
        for probe in probes:
            if probe.name == str(metadata["probe_id"]):
                device = probe
                break
        map_list = []
        for map_element in metadata['map'].keys():
            map_list.append((map_element, metadata['map'][map_element]))

        electrode_group = NTrode(
            probe_id=metadata["probe_id"],
            ntrode_id=metadata['ntrode_id'],
            device=device,
            location='-',
            description='-',
            name='ntrode ' + str(metadata['ntrode_id']),
            map=map_list
        )
        return electrode_group

    def __add_devices(self, content):
        probes = []
        for fl_probe in self.probes:
            probes.append(Probe(
                probe_type=fl_probe["probe_type"],
                contact_size=fl_probe["contact_size"],
                num_shanks=fl_probe['num_shanks'],
                id=fl_probe["id"],
                name=str(fl_probe["id"])
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

    def __build_aparatus(self, content):
        apparatus_columns = []
        for counter, row in enumerate(self.metadata['apparatus']['data']):
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
        for task in self.metadata['tasks']:
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
