from hdmf.common import VectorData, DynamicTable
from mountainlab_pytools.mdaio import readmda
from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

import src.datamigration.file_scanner as fs
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_builder.pos_extractor import POSExtractor


class NWBFileBuilder:
    def __init__(self, data_path, animal_name, date, dataset, output_file_path='output.nwb'):
        self.data_folder = fs.DataScanner(data_path)
        self.mda_path = self.data_folder.data[animal_name][date][dataset].get_data_path_from_dataset('mda')
        self.mda_timestamps_path = self.data_folder.get_mda_timestamps(animal_name, date, dataset)
        self.mda_file_count = len(self.data_folder.data[animal_name][date][dataset].
                                  get_all_data_from_dataset('mda')) - 2  # timestamp and log files are not counted
        self.output_file_path = output_file_path

        for file in self.data_folder.data[animal_name][date][dataset].get_all_data_from_dataset('pos'):
            if file.endswith('pos_online.dat'):
                self.pos_extractor = POSExtractor(self.data_folder.data[animal_name][date][dataset].
                                                  get_data_path_from_dataset('pos') + file)

        metadata_extractor = MetadataExtractor(self.data_folder.get_metadata(animal_name, date, dataset))

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

    def build(self, mda_data_chunk_size=1):
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
            apparatus_columns.append(VectorData(name='col ' + str(counter), description='', data=self.apparatus[counter]))
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

        with NWBHDF5IO(path=self.output_file_path, mode='w') as nwb_fileIO:
            nwb_fileIO.write(nwb_file_content)
            nwb_fileIO.close()

        timestamps = readmda(self.mda_timestamps_path)
        mda_extractor = MdaExtractor(self.mda_path, timestamps)
        file_number = 0
        while file_number < self.mda_file_count:  # switch to function from file scanner after its merged into master
            with NWBHDF5IO(path=self.output_file_path, mode='a') as IO:
                nwb_fileIO = IO.read()
                electrode_table_region = nwb_fileIO.create_electrode_table_region([0], "sample description")
                for series in mda_extractor.get_mda(file_number, mda_data_chunk_size, electrode_table_region):
                    nwb_fileIO.add_acquisition(series)
                IO.write(nwb_fileIO)
                IO.close()
            file_number = file_number + mda_data_chunk_size
        return self.output_file_path