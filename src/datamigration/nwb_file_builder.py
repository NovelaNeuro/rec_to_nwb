import datetime
import logging
import os
import uuid

from hdmf.common import DynamicTable
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.node import Node
from src.datamigration.extension.ntrode import NTrode
from src.datamigration.extension.probe import Probe
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.builders.apparatus_builder import build_apparatus
from src.datamigration.nwb_builder.builders.dio_builder import build_dio
from src.datamigration.nwb_builder.builders.mda_builder import build_mda
from src.datamigration.nwb_builder.builders.ntrodes_builder import build_ntrodes
from src.datamigration.nwb_builder.builders.pos_builder import build_position
from src.datamigration.nwb_builder.builders.processing_module_builder import build_processing_module
from src.datamigration.nwb_builder.builders.task_builder import build_task
from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.electrode_addentum import ElectrodeAddendum
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_checker import check_headers_compatibility
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_reader import HeaderReader
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder
from src.datamigration.nwb_builder.extractors.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.extractors.pos_extractor import POSExtractor
from src.datamigration.nwb_builder.extractors.xml_extractor import XMLExtractor

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self, data_path, animal_name, date, nwb_metadata, output_file='output.nwb', process_dio=True, process_mda=True):
        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_folder = fs.DataScanner(data_path)
        self.dataset_names = self.data_folder.get_all_datasets(animal_name, date)
        self.datasets = [self.data_folder.data[animal_name][date][dataset_mda] for dataset_mda in self.dataset_names]
        self.process_dio = process_dio
        self.process_mda = process_mda

        self.output_file = output_file

        self.metadata = nwb_metadata.metadata
        self.probes = nwb_metadata.probes

        check_headers_compatibility(self.data_path, self.animal_name, self.date)

        self.header = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                             self.date + '/header.xml')
        self.spike_n_trodes = self.header.configuration.spike_configuration.spike_n_trodes

    def build(self):
        nwb_content = NWBFile(session_description=self.metadata['session description'],
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
        build_processing_module('behavior', 'processing module for all behavior-related data', nwb_content)

        build_task(self.metadata, nwb_content)

        build_position(self.datasets, nwb_content)

        build_apparatus(self.metadata, nwb_content)

        self.__build_general(nwb_content)

        build_ntrodes(self.metadata, nwb_content)

        if self.process_dio:
            build_dio(self.metadata,
                      self.data_path + '/' + self.animal_name + '/preprocessing/' + self.date,
                      nwb_content)

        if self.process_mda:
            build_mda(self.header,
                      self.metadata,
                      self.datasets,
                      nwb_content)

        return nwb_content

    def __build_general(self, content):
        """
            For each electrode group in metadata.yml, check if device exist.
            If not create one.
            Create electrode_group
            Create electrodes from corresponding probe_type in probe.yml
        """

        device_counter = 0
        electrode_addendum = ElectrodeAddendum()

        for electrode_group_metadata in self.metadata['electrode groups']:
            device = self.__check_device(content, electrode_group_metadata['device_type'], device_counter)
            electrode_group = self.__create_electrode_group(content, electrode_group_metadata, device)
            self.__create_electrodes(content, electrode_group, electrode_group_metadata['device_type'],
                                     electrode_addendum)

        self.add_extensions_to_electrodes(content, electrode_addendum)

    def __check_device(self, content, device_type, device_counter):
        for device_name in content.devices:
            device = content.get_device(device_name)
            if device.probe_type == device_type:
                return device
        return self.__create_device(content, device_type, device_counter)

    def __create_device(self, content, device_type, device_counter):
        probe = None
        for fl_probe in self.probes:
            if fl_probe['probe_type'] == device_type:
                probe = Probe(
                    probe_type=fl_probe["probe_type"],
                    contact_size=fl_probe["contact_size"],
                    num_shanks=fl_probe['num_shanks'],
                    id=device_counter,
                    name=str(device_counter)
                )
        content.add_device(probe)
        device_counter += 1

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

    def __create_electrodes(self, content, electrode_group, device_type, electrode_addendum):
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
                                id=electrode_addendum.electrode_counter)
                        electrode_addendum.rel_x.append(electrode['rel_x'])
                        electrode_addendum.rel_y.append(electrode['rel_y'])
                        electrode_addendum.rel_z.append(electrode['rel_z'])
                        electrode_addendum.electrode_counter += 1

    def add_extensions_to_electrodes(self, content, electrode_addendum):
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
            data=electrode_addendum.rel_x
        )

        content.electrodes.add_column(
            name='rel_y',
            description='None',
            data=electrode_addendum.rel_y
        )

        content.electrodes.add_column(
            name='rel_z',
            description='None',
            data=electrode_addendum.rel_z
        )

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
