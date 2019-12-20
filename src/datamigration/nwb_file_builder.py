import logging
import os

from hdmf.common import VectorData, DynamicTable
from pynwb import NWBHDF5IO, NWBFile

import src.datamigration.file_scanner as fs
from src.datamigration.extension.probe import Probe
from src.datamigration.extension.shank import Shank
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.header_checker.rec_file_finder import RecFileFinder
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor
from src.datamigration.nwb_builder.header_checker.rec_file_finder import RecFileFinder
from src.datamigration.nwb_builder.header_checker.header_comparator import HeaderComparator
from src.datamigration.xml_extractor import XMLExtractor

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self, data_path, animal_name, date, dataset, metadata_path, output_file='output.nwb'):
        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_folder = fs.DataScanner(data_path)
        self.dataset_names = self.data_folder.get_all_datasets(animal_name, date)
        self.datasets = [self.data_folder.data[animal_name][date][dataset_mda] for dataset_mda in self.dataset_names]

        self.mda_timestamps_path = self.data_folder.get_mda_timestamps(animal_name, date, dataset)
        self.output_file = output_file

        self.metadata = MetadataExtractor(config_path=metadata_path)
        self.spike_n_trodes = Header('header.xml').configuration.spike_configuration.spike_n_trodes

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

        # ToDo : task building with new metadata ---self.__build_task(content)

        self.__check_headers_compatibility()

        self.__build_position(content)

        self.__build_aparatus(content)

        probes = self.__add_devices(content)

        self.__build_shanks(content, probes, self.spike_n_trodes)

        self.__add_electrodes(content)

        self.__build_dio(content)

        self.__add_electrodes_extensions(content, self.spike_n_trodes)

        self.__build_mda(content)
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
            differences = header_reader.headers_differences
            logging.warning(message, differences,)

        XMLExtractor(rec_path=rec_files[0], xml_path='header.xml').extract_xml_from_rec_file()

    def __create_region(self, content):
        region = content.create_electrode_table_region(
            description=self.metadata.electrode_regions[0]['description'],
            region=self.metadata.electrode_regions[0]['region'])
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

    def __build_shanks(self, content, probes, spike_n_trodes):
        shanks = []
        for group_index, electrode_group_dict in enumerate(self.metadata.electrode_groups):
            shank = self.__create_shank(electrode_group_dict, group_index, probes, spike_n_trodes)
            shanks.append(shank)
        for shank in shanks:
            content.add_electrode_group(shank)

    @staticmethod
    def __create_shank(electrode_group_dict, group_index, probes, spike_n_trodes):
        shank = Shank(
            name=str(electrode_group_dict['name']),
            description=electrode_group_dict['description'],
            location=electrode_group_dict['location'],
            device=[probe for probe in probes
                    if probe.name == electrode_group_dict['device']][0],
            filterOn=spike_n_trodes[group_index].filter_on,
            lowFilter=spike_n_trodes[group_index].low_filter,
            lfpRefOn=spike_n_trodes[group_index].lfp_ref_on,
            color=spike_n_trodes[group_index].color,
            highFilter=spike_n_trodes[group_index].hight_filter,
            lfpFilterOn=spike_n_trodes[group_index].lfp_filter_on,
            moduleDataOn=spike_n_trodes[group_index].module_data_on,
            LFPHighFilter=spike_n_trodes[group_index].lfp_high_filter,
            refGroup=spike_n_trodes[group_index].ref_group,
            LFPChan=spike_n_trodes[group_index].lfp_chan,
            refNTrodeID=spike_n_trodes[group_index].ref_n_trode_id,
            refChan=spike_n_trodes[group_index].ref_chan,
            groupRefOn=spike_n_trodes[group_index].group_ref_on,
            refOn=spike_n_trodes[group_index].ref_on,
            id=str(spike_n_trodes[group_index].id),
        )
        return shank

    def __add_devices(self, content):
        probes = []
        for counter, device_name in enumerate(self.metadata.devices):
            probes.append(Probe(
                name=device_name,
                probe_id=str(counter)
            )
            )

        for probe in probes:
            content.add_device(probe)
        return probes

    def __build_mda(self, content):
        sampling_rate = Header('header.xml').configuration.hardware_configuration.sampling_rate
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
        content.create_processing_module(
            name='task',
            description='Sample description'
        ).add_data_interface(self.metadata.task)

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
