import logging
import os

from hdmf.common import VectorData, DynamicTable
from mountainlab_pytools.mdaio import readmda
from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

import src.datamigration.file_scanner as fs
from src.datamigration.extension.probe import Probe
from src.datamigration.extension.shank import Shank
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor


class NWBFileBuilder:
    def __init__(self, data_path, animal_name, date, dataset, config_path, xml_path, output_file_location='',
                 output_file_name='output.nwb'):
        self.data_folder = fs.DataScanner(data_path)
        self.mda_path = self.data_folder.data[animal_name][date][dataset].get_data_path_from_dataset('mda')
        self.mda_timestamps_path = self.data_folder.get_mda_timestamps(animal_name, date, dataset)
        self.mda_file_count = len(self.data_folder.data[animal_name][date][dataset].
                                  get_all_data_from_dataset('mda')) - 2  # timestamp and logging files are not counted
        self.output_file_location = output_file_location
        self.output_file_path = output_file_location + output_file_name

        for file in self.data_folder.data[animal_name][date][dataset].get_all_data_from_dataset('pos'):
            if file.endswith('pos_online.dat'):
                self.pos_extractor = POSExtractor(self.data_folder.data[animal_name][date][dataset].
                                                  get_data_path_from_dataset('pos') + file)
        self.metadata = MetadataExtractor(config_path)

    def build(self):
        logging.info("Begining nwb file build" + '\n')
        logging.info(
            "File Location:" + '\n' + os.path.abspath(self.output_file_location + self.output_file_path + '\n'))

        nwb_file_content = NWBFile(session_description=self.metadata.session_description,
                                   experimenter=self.metadata.experimenter_name,
                                   lab=self.metadata.lab,
                                   institution=self.metadata.institution,
                                   session_start_time=self.metadata.session_start_time,
                                   identifier=str(self.metadata.identifier),
                                   experiment_description=self.metadata.experiment_description,
                                   subject=self.metadata.subject,
                                   )

        task_module = ProcessingModule(name='task', description='Sample description')
        nwb_file_content.add_processing_module(task_module).add(self.metadata.task)

        position_module = ProcessingModule(name='position', description='Sample description')
        position = self.pos_extractor.get_position()
        nwb_file_content.add_processing_module(position_module).add_data_interface(position)

        apparatus_columns = []
        for counter, row in enumerate(self.metadata.apparatus):
            apparatus_columns.append(VectorData(name='col ' + str(counter), description='', data=row))
        apparatus_dynamic_table = DynamicTable(
            name='apparatus',
            description='Sample description',
            id=None,
            columns=apparatus_columns
        )
        apparatus_module = ProcessingModule(name='apparatus', description='Sample description')
        apparatus_module.add(apparatus_dynamic_table)
        nwb_file_content.add_processing_module(apparatus_module)

        for counter, device_name in enumerate(self.metadata.devices):
            nwb_file_content.add_device(
                Probe(
                    name=device_name,
                    probe_id=str(counter)
                )
            )

        maxDisp = []
        triggerOn = []
        hwChan = []
        thresh = []
        for group_index, electrode_group_dict in enumerate(self.metadata.electrode_groups):
            spike_channels = self.spike_n_trodes[group_index].spike_channels

            nwb_file_content.add_electrode_group(
                Shank(
                    name=electrode_group_dict['name'],
                    description=electrode_group_dict['description'],
                    location=electrode_group_dict['location'],
                    device=[nwb_file_content.devices[device_name] for device_name in nwb_file_content.devices
                            if device_name == electrode_group_dict['device']][0],
                    filterOn=self.spike_n_trodes[group_index].filter_on,
                    lowFilter=self.spike_n_trodes[group_index].low_filter,
                    lfpRefOn=self.spike_n_trodes[group_index].lfp_ref_on,
                    color=self.spike_n_trodes[group_index].color,
                    highFilter=self.spike_n_trodes[group_index].hight_filter,
                    lfpFilterOn=self.spike_n_trodes[group_index].lfp_filter_on,
                    moduleDataOn=self.spike_n_trodes[group_index].module_data_on,
                    LFPHighFilter=self.spike_n_trodes[group_index].lfp_high_filter,
                    refGroup=self.spike_n_trodes[group_index].ref_group,
                    LFPChan=self.spike_n_trodes[group_index].lfp_chan,
                    refNTrodeID=self.spike_n_trodes[group_index].ref_n_trode_id,
                    refChan=self.spike_n_trodes[group_index].ref_chan,
                    groupRefOn=self.spike_n_trodes[group_index].group_ref_on,
                    refOn=self.spike_n_trodes[group_index].ref_on,
                    id=self.spike_n_trodes[group_index].id,
                )
            )

            for spike_channel in spike_channels:
                maxDisp.append(spike_channel.max_disp)
                triggerOn.append(spike_channel.trigger_on)
                hwChan.append(spike_channel.hw_chan)
                thresh.append(spike_channel.thresh)

        for electrode in self.metadata.electrodes:
            nwb_file_content.add_electrode(
                x=electrode['x'],
                y=electrode['y'],
                z=electrode['z'],
                imp=electrode['imp'],
                location=electrode['location'],
                filtering=electrode['filtering'],
                group=[nwb_file_content.electrode_groups[group_name] for group_name in nwb_file_content.electrode_groups
                       if group_name == electrode['group']][0],
                id=electrode['id'],
            )

        nwb_file_content.electrodes.add_column(
            name='maxDisp',
            description='maxDisp sample description',
            data=maxDisp
        )
        nwb_file_content.electrodes.add_column(
            name='thresh',
            description='thresh sample description',
            data=thresh
        )
        nwb_file_content.electrodes.add_column(
            name='hwChan',
            description='hwChan sample description',
            data=hwChan
        )
        nwb_file_content.electrodes.add_column(
            name='triggerOn',
            description='triggerOn sample description',
            data=triggerOn
        )

        for electrode_region in self.metadata.electrode_regions:
            nwb_file_content.create_electrode_table_region(
                name=electrode_region['name'],
                description=electrode_region['description'],
                region=electrode_region['region']
            )

        logging.info("begining mda extraction" + '\n')

        timestamps = readmda(self.mda_timestamps_path)
        mda_extractor = MdaExtractor(self.mda_path, timestamps)

        electrode_table_region = nwb_file_content.create_electrode_table_region([0, 1], "first and second electrode")
        series = mda_extractor.get_mda(electrode_table_region)
        nwb_file_content.add_acquisition(series)
        return nwb_file_content

    def write(self, content):
        with NWBHDF5IO(path=self.output_file_path, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file_path
