from hdmf.common import VectorData, DynamicTable
from mountainlab_pytools.mdaio import readmda
from pynwb import NWBHDF5IO, NWBFile

import src.datamigration.file_scanner as fs
from src.datamigration.extension.probe import Probe
from src.datamigration.extension.shank import Shank
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor


class NWBFileBuilder:

    def __init__(self, data_path, animal_name, date, dataset, config_path, header_path, output_file='output.nwb'):
        self.data_folder = fs.DataScanner(data_path)
        self.mda_paths = [];
        for current_dataset in self.data_folder.get_all_datasets(animal_name, date):
            self.mda_paths.append(
                self.data_folder.data[animal_name][date][current_dataset].get_data_path_from_dataset('mda'))
        self.mda_timestamps_path = self.data_folder.get_mda_timestamps(animal_name, date, dataset)
        self.output_file = output_file

        for file in self.data_folder.data[animal_name][date][dataset].get_all_data_from_dataset('pos'):
            if file.endswith('pos_online.dat'):
                self.pos_extractor = POSExtractor(self.data_folder.data[animal_name][date][dataset].
                                                  get_data_path_from_dataset('pos') + file)
        self.metadata = MetadataExtractor(config_path)
        self.header_path = header_path
        self.spike_n_trodes = Header(header_path).configuration.spike_configuration.spike_n_trodes

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

        self.__build_aparatus(content)

        probes = self.__add_devices(content)

        self.__build_shanks(content, probes, self.spike_n_trodes)

        self.__add_electrodes(content)

        self.__add_electrodes_extensions(content, self.spike_n_trodes)

        self.__build_mda(content)
        return content

    def __create_region(self, content):
        region = content.create_electrode_table_region(
            description=self.metadata.electrode_regions[0]['description'],
            region=self.metadata.electrode_regions[0]['region'])
        return region

    def __add_electrodes_extensions(self, content, spike_n_trodes):
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
                imp=electrode['imp'],
                location=electrode['location'],
                filtering=electrode['filtering'],
                group=[content.electrode_groups[group_name] for group_name in content.electrode_groups
                       if group_name == electrode['group']][0],
                id=electrode['id'],
            )

    def __build_shanks(self, content, probes, spike_n_trodes):
        shanks = []
        for group_index, electrode_group_dict in enumerate(self.metadata.electrode_groups):
            shank = self.__create_shank(electrode_group_dict, group_index, probes, spike_n_trodes)
            shanks.append(shank)
        for shank in shanks:
            content.add_electrode_group(shank)

    def __create_shank(self, electrode_group_dict, group_index, probes, spike_n_trodes):
        shank = Shank(
            name=electrode_group_dict['name'],
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
            id=spike_n_trodes[group_index].id,
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
        timestamps = readmda(self.mda_timestamps_path)
        mda_extractor = MdaExtractor(self.mda_paths, timestamps)
        electrode_table_region = self.__create_region(content)
        series = mda_extractor.get_mda(electrode_table_region)
        content.add_acquisition(series)

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
        content.create_processing_module(
            name='position',
            description='Sample description'
        ).add_data_interface(
            self.pos_extractor.get_position()
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
