from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor


class NWBFileCreator:

    def __init__(self, pos_path, metadata_path, mda_path, mda_timestamp_name, output_file_path='output.nwb'):

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

        nwb_file_content.add(self.apparatus)

        # ToDo check if exist
        for device_name in self.devices:
            nwb_file_content.create_device(name=device_name)

        for electrode_group_dict in self.electrode_groups:
            nwb_file_content.create_electrode_group(
                name=electrode_group_dict['name'],
                description=electrode_group_dict['description'],
                location=electrode_group_dict['location'],
                device=[nwb_file_content.devices[device_name] for device_name in nwb_file_content.devices
                        if device_name == electrode_group_dict['device']][0]
            )

        for electrode in self.electrodes:
            nwb_file_content.add_electrode(
                x=electrode['x'],
                y=electrode['y'],
                z=electrode['z'],
                imp=electrode['imp'],
                location=electrode['location'],
                filtering=electrode['filtering'],
                group=[nwb_file_content.electrode_groups[group_name] for group_name in nwb_file_content.electrode_groups
                       if group_name == electrode['group']][0],
                id=electrode['id']
            )

        for electrode_region in self.electrode_regions:
            nwb_file_content.create_electrode_table_region(
                name=electrode_region['name'],
                description=electrode_region['description'],
                region=electrode_region['region']
            )

        #
        # # todo Temporary hard-coded table_region
        # electrode_table_region = nwb_file_content.create_electrode_table_region([0], "sample description")
        #
        # series_table = MdaExtractor(self.mda_path, self.mda_timestamp_path, electrode_table_region)
        # for series in series_table.get_mda():
        #     nwb_file_content.add_acquisition(series)

        with NWBHDF5IO(self.output_file_path, mode='w') as nwb_fileIO:
            nwb_fileIO.write(nwb_file_content)

        return self.output_file_path


