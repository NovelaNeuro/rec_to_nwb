import datetime
import logging
import os
import uuid

from hdmf.common import DynamicTable
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.file_scanner as fs
from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.node import Node
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

        self.metadata = nwb_metadata.metadata
        self.probes = nwb_metadata.probes
        self.__check_headers_compatibility()
        self.header = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                             self.date + '/header.xml')
        self.spike_n_trodes = self.header.configuration.spike_configuration.spike_n_trodes

        self.global_device_counter = 0
        self.global_electrode_counter = 0
        self.rel_x = []
        self.rel_y = []
        self.rel_z = []

    def build(self):
        content = NWBFile(session_description=self.metadata['session description'],
                          experimenter=self.metadata['experimenter name'],
                          lab=self.metadata['lab'],
                          institution=self.metadata['institution'],
                          session_start_time=datetime.datetime.strptime(
                              self.metadata['session start time'], '%m/%d/%Y %H:%M:%S'
                          ),
                          identifier=str(uuid.uuid1()),
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
        self.__create_processing_module(content)

        self.__build_task(content)

        self.__build_position(content)

        self.__build_apparatus(content)

        self.__build_general(content)

        self.__build_ntrodes(content)

        self.__build_dio(content)

        self.__build_mda(content)

        return content

    @staticmethod
    def __create_processing_module(content):
        content.create_processing_module(
            name='behavior',
            description='processing module for all behavior-related data'
        )

    def __check_headers_compatibility(self, ):
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
            logging.warning(message, differences, )
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
            # name=self.metadata['electrode region']['name']
            name='electrodes'
        )
        return region

    def __build_general(self, content):
        """
            For each electrode group in metadata.yml, check if device exist.
            If not create one.
            Create electrode_group
            Create electrodes from corresponding probe_type in probe.yml
        """
        for electrode_group_metadata in self.metadata['electrode groups']:
            device = self.__check_device(content, electrode_group_metadata['device_type'])
            electrode_group = self.__create_electrode_group(content, electrode_group_metadata, device)
            self.__create_electrodes(content, electrode_group, electrode_group_metadata['device_type'])

        self.add_extensions_to_electrodes(content)

    def __check_device(self, content, device_type):
        for device_name in content.devices:
            device = content.get_device(device_name)
            if device.probe_type == device_type:
                return device
        return self.__create_device(content, device_type)

    def __create_device(self, content, device_type):
        probe = None
        for fl_probe in self.probes:
            if fl_probe['probe_type'] == device_type:
                probe = Probe(
                    probe_type=fl_probe["probe_type"],
                    contact_size=fl_probe["contact_size"],
                    num_shanks=fl_probe['num_shanks'],
                    id=self.global_device_counter,
                    name=str(self.global_device_counter)
                )
        content.add_device(probe)
        self.global_device_counter += 1

        return probe

    @staticmethod
    def __create_electrode_group(content, metadata, device):
        electrode_group = FLElectrodeGroup(
            id=metadata['id'],
            device=device,
            location=str(metadata['location']),
            description=str(metadata['description']),
            name='electrode group ' + str(metadata["id"])
        )
        content.add_electrode_group(electrode_group)
        return electrode_group

    def __create_electrodes(self, content, electrode_group, device_type):
        for fl_probe in self.probes:
            if fl_probe['probe_type'] == device_type:

                for shank in fl_probe['shanks']:
                    for electrode in shank['electrodes']:
                        content.add_electrode(
                                x=0.0,
                                y=0.0,
                                z=0.0,
                                imp=1.0,
                                location='None',
                                filtering='None',
                                group=electrode_group,
                                id=self.global_electrode_counter)
                        self.rel_x.append(electrode['rel_x'])
                        self.rel_y.append(electrode['rel_y'])
                        self.rel_z.append(electrode['rel_z'])
                        self.global_electrode_counter += 1

    def add_extensions_to_electrodes(self, content):
        spike_channels_list = []
        hw_chan = []
        for spike_n_trode in self.header.configuration.spike_configuration.spike_n_trodes:
            for spike_channel in spike_n_trode.spike_channels:
                spike_channels_list.append(spike_channel)

        for spike_channel, electrode in zip(spike_channels_list, content.electrodes):
            hw_chan.append(spike_channel.hw_chan)


        content.electrodes.add_column(
            name='hwChan',
            description='None',
            data=hw_chan
        )

        content.electrodes.add_column(
            name='rel_x',
            description='None',
            data=self.rel_x
        )

        content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=self.rel_y
        )

        content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=self.rel_z
        )


    def __build_ntrodes(self, content):
        fl_ntrodes = []
        for ntrode_metadata in self.metadata['ntrode probe channel map']:
            fl_ntrode = self.__create_ntrode(ntrode_metadata, content.devices)
            fl_ntrodes.append(fl_ntrode)
        for fl_ntrode in fl_ntrodes:
            content.add_electrode_group(fl_ntrode)

    @staticmethod
    def __create_ntrode(metadata, devices):
        probe_id = str(metadata["probe_id"])
        device = devices[probe_id]

        map_list = []
        for map_element in metadata['map'].keys():
            map_list.append((map_element, metadata['map'][map_element]))

        ntrode = NTrode(
            probe_id=metadata["probe_id"],
            ntrode_id=metadata['ntrode_id'],
            device=device,
            location='-',
            description='-',
            name='ntrode ' + str(metadata['ntrode_id']),
            map=map_list
        )
        return ntrode

    def __build_mda(self, content):
        sampling_rate = self.header.configuration.hardware_configuration.sampling_rate
        experiment_start_time = datetime.datetime.strptime(
            self.metadata['session start time'], '%m/%d/%Y %H:%M:%S')
        mda_extractor = MdaExtractor(self.datasets, experiment_start_time)
        electrode_table_region = self.__create_region(content)
        series = mda_extractor.get_mda(electrode_table_region, sampling_rate)
        content.add_acquisition(series)

    def __build_dio(self, content):
        extracted_dio = DioExtractor(data_path=self.data_path + '/' + self.animal_name + '/preprocessing/' + self.date,
                                     metadata=self.metadata)
        content.processing["behavior"].add_data_interface(
            extracted_dio.get_dio()
        )

    def __build_apparatus(self, content):
        nodes = []
        edges = []
        col_nodes = []
        global_counter = 0
        for row_counter, row in enumerate(self.metadata['apparatus']['data']):
            for col_counter, col in enumerate(row):
                col_nodes.append(
                    Node(
                        name='node' + str(global_counter),
                        value=col
                    )
                )
                global_counter = global_counter + 1

            nodes.extend(col_nodes)
            edges.append(
                Edge(
                    name='edge' + str(row_counter),
                    edge_nodes=col_nodes
                )
            )
            col_nodes = []

        content.processing["behavior"].add_data_interface(
            Apparatus(
                name='apparatus',
                edges=edges,
                nodes=nodes
            )
        )

    def __build_position(self, content):
        pos_extractor = POSExtractor(self.datasets)
        content.processing["behavior"].add_data_interface(
            pos_extractor.get_position()
        )

    def __build_task(self, content):
        nwb_table = DynamicTable(
            name='task',
            description='None',
        )

        nwb_table.add_column(
            name='task_name',
            description='None',
        )
        nwb_table.add_column(
            name='task_description',
            description='None',
        )
        for task in self.metadata['tasks']:
            nwb_table.add_row(task)

        content.processing['behavior'].add_data_interface(nwb_table)

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
