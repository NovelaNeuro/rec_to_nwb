from hdmf.common import VectorData, DynamicTable
from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

from src.datamigration.header.module.header import Header
from src.datamigration.models.FLElectrodes import FLElectrodes, FLElectrodesContainer
from src.datamigration.models.FLElectrodesGroup import FLElectrodesGroup, FLElectrodesGroupContainer
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor


class NWBFileBuilder:

    def __init__(self, pos_path, metadata_path, mda_path, mda_timestamp_name, xml_path, output_file_path='output.nwb'):

        self.mda_path = mda_path
        self.mda_timestamp_path = mda_timestamp_name
        self.output_file_path = output_file_path

        self.pos_extractor = POSExtractor(pos_path)

        metadata_extractor = MetadataExtractor(metadata_path)

        self.experimenter_name = metadata_extractor.experimenter_name
        self.lab = metadata_extractor.lab
        self.institution = metadata_extractor.institution
        self.experiment_description = metadata_extractor.experiment_description
        self.session_description = metadata_extractor.session_description
        self.session_start_time = metadata_extractor.session_start_time
        self.identifier = str(metadata_extractor.identifier)

        self.task = metadata_extractor.task
        self.subject = metadata_extractor.subject
        self.apparatus = metadata_extractor.apparatus

        self.devices = metadata_extractor.devices
        self.electrode_groups = metadata_extractor.electrode_groups
        self.electrodes = metadata_extractor.electrodes
        self.electrode_regions = metadata_extractor.electrode_regions

        self.spike_n_trodes = Header(xml_path).configuration.spike_configuration.spike_n_trodes


    def build(self):
        nwb_file_content = NWBFile(session_description=self.session_description,
                                   experimenter=self.experimenter_name,
                                   lab=self.lab,
                                   institution=self.institution,
                                   session_start_time=self.session_start_time,
                                   identifier=self.identifier,
                                   experiment_description=self.experiment_description,
                                   subject=self.subject,
                                   )

        task_module = ProcessingModule(name='task', description='Sample description')
        nwb_file_content.add_processing_module(task_module).add(self.task)

        position_module = ProcessingModule(name='position', description='Sample description')
        position = self.pos_extractor.get_position()
        nwb_file_content.add_processing_module(position_module).add(position)

        apparatus_columns = []
        for counter in range(len(self.apparatus)):
            apparatus_columns.append(
                VectorData(name='col ' + str(counter), description='', data=self.apparatus[counter]))
        apparatus_dynamic_table = DynamicTable(
            name='apparatus',
            description='Sample description',
            id=None,
            columns=apparatus_columns
        )
        apparatus_module = ProcessingModule(name='apparatus', description='Sample description')
        apparatus_module.add_container(apparatus_dynamic_table)
        nwb_file_content.add_processing_module(apparatus_module)

        for device_name in self.devices:
            nwb_file_content.create_device(name=device_name)



        electrode_counter = 0
        fl_electrode_group_container = FLElectrodesGroupContainer()
        for group_index in range(len(self.spike_n_trodes)):
            electrode_group = (
                FLElectrodesGroup(
                    name='ElectrodeGroup ' + self.spike_n_trodes[group_index].id,
                    description='description',
                    location='location',
                    device=nwb_file_content.devices['dev1'],
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
            fl_electrode_group_container.add_electrodes_group(electrode_group)

            fl_electrode_container = FLElectrodesContainer()
            spike_channels = self.spike_n_trodes[group_index].spike_channels
            for electrode_index in (range(len(spike_channels))):
                fl_electrode_container.add_electrodes(
                    FLElectrodes(
                        name='Electrode ' + str(electrode_counter),
                        x=1.0,
                        y=1.0,
                        z=1.0,
                        imp=1.0,
                        location='sample location',
                        filtering='sample filtering',
                        group=electrode_group,
                        id=electrode_counter,
                        maxDisp=spike_channels[electrode_index].max_disp,
                        triggerOn=spike_channels[electrode_index].trigger_on,
                        hwChan=spike_channels[electrode_index].hw_chan,
                        thresh=spike_channels[electrode_index].thresh,
                    )
                )
                electrode_counter = electrode_counter + 1
        print(fl_electrode_group_container)
        # print(fl_electrode_container)
        # fl_electrode = FLElectrode(
        #     name='Electrode ',
        #     x=1.0,
        #     y=2.0,
        #     z=3.0,
        #     imp=4.0,
        #     location='sample location',
        #     filtering='sample filtering',
        #     group=fl_electrodes_group,
        #     id=1,
        #     maxDisp=1,
        # )
        # electrode_group_module = ProcessingModule(name='electrode_group', description='Sample description')
        # electrode_group_module.add_container(fl_electrodes_group)
        # nwb_file_content.add_processing_module(electrode_group_module)

        # for electrode in self.electrodes:
        #         flElectrode(
        #             x=1.0,
        #             y=2.0,
        #             z=3.0,
        #             imp=4.0,
        #             location=electrode['location'],
        #             filtering=electrode['filtering'],
        #             group=
        #             [nwb_file_content.electrode_groups[group_name] for group_name in nwb_file_content.electrode_groups
        #              if group_name == electrode['group']][0],
        #             id=electrode['id'],
        #             maxDisp=123,
        #             name='Electrode ' + str(electrode['id'])
        #         ))

        #
        # for electrode_group_dict in self.electrode_groups:
        #     nwb_file_content.create_electrode_group(
        #         name=electrode_group_dict['name'],
        #         description=electrode_group_dict['description'],
        #         location=electrode_group_dict['location'],
        #         device=[nwb_file_content.devices[device_name] for device_name in nwb_file_content.devices
        #                 if device_name == electrode_group_dict['device']][0]
        #     )
        #
        # for electrode in self.electrodes:
        #     nwb_file_content.add_electrode(
        #         x=electrode['x'],
        #         y=electrode['y'],
        #         z=electrode['z'],
        #         imp=electrode['imp'],
        #         location=electrode['location'],
        #         filtering=electrode['filtering'],
        #         group=[nwb_file_content.electrode_groups[group_name] for group_name in nwb_file_content.electrode_groups
        #                if group_name == electrode['group']][0],
        #         id=electrode['id']
        #     )

        # for electrode_region in self.electrode_regions:
        #     nwb_file_content.create_electrode_table_region(
        #         name=electrode_region['name'],
        #         description=electrode_region['description'],
        #         region=electrode_region['region']
        #     )
        #
        # electrode_table_region = nwb_file_content.create_electrode_table_region([0], "sample description")
        #
        # series_table = MdaExtractor(self.mda_path, self.mda_timestamp_path, electrode_table_region)
        # for series in series_table.get_mda():
        #     nwb_file_content.add_acquisition(series)

        with NWBHDF5IO(path=self.output_file_path, mode='w') as nwb_fileIO:
            nwb_fileIO.write(nwb_file_content)

        return self.output_file_path
