from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

from src.datamigration.nwb.metadata_extractor import MetadataExtractor
from src.datamigration.nwb.pos_extractor import POSExtractor
import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import NWBHDF5IO, NWBFile, ProcessingModule, ecephys


from src.e2etests.integration.experiment_data import \
    ExperimentData  # todo you cannot use ExperimentData in implementation!!!This is only for tests!


class NWBFileCreator:


    def __init__(self, pos_path, metadata_path, output_file_path='output_sample.nwb'):

        self.position = POSExtractor(pos_path).get_position()

        metadata_extractor = MetadataExtractor(metadata_path)

        self.output_file_path = output_file_path
        self.experimenter_name = metadata_extractor.experimenter_name
        self.lab = metadata_extractor.lab
        self.institution = metadata_extractor.institution
        self.experiment_description = metadata_extractor.experiment_description
        self.session_description = metadata_extractor.session_description
        self.session_start_time = metadata_extractor.session_start_time
        self.identifier = str(metadata_extractor.identifier)

        self.task = metadata_extractor.task
        self.subject = metadata_extractor.subject

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

        task_module = ProcessingModule(name='task', description='testDescription')
        nwb_file_content.add_processing_module(task_module).add(self.task)

        position_module = ProcessingModule(name='position', description='testDescription')
        nwb_file_content.add_processing_module(position_module).add(self.position)

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
        # timestamps = readmda(
        #     '../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.mda/' + ExperimentData.mda_timestamp)
        # mda_files = [mda_file for mda_file in
        #              os.listdir('../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.mda/') if
        #              (mda_file.endswith('.mda') and mda_file != ExperimentData.mda_timestamp)]
        #
        # electrode_table_region = nwb_file_content.create_electrode_table_region([0, 1], "description")
        # data_len = 1000
        # rate = 10.0
        # ephys_timestamps = np.arange(data_len) / rate
        # timestamps_list = timestamps.tolist()
        # counter = 0
        # counter_time = 0
        # for file in mda_files:
        #     for i in range(4):
        #         counter_time = counter_time + 1
        #         name = "test " + str(counter * 4 + i)
        #
        #         series = ecephys.ElectricalSeries(name,
        #                                           readmda(
        #                                               '../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.mda/' + file)[
        #                                               i],
        #                                           electrode_table_region,
        #                                           timestamps=timestamps_list,
        #                                           resolution=0.001,
        #                                           comments=name,
        #                                           description="Electrical series registered on electrode " + str(
        #                                               counter * 4 + i))
        #         nwb_file_content.add_acquisition(series)
        #     counter = counter + 1

        with NWBHDF5IO(self.output_file_path, mode='w') as nwb_fileIO:
            nwb_fileIO.write(nwb_file_content)

        return self.output_file_path



# if __name__ == '__main__':
#     obj = NWBFileCreator(
#         '../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.1.pos/20190718_beans_01_s1.1.pos_online.dat',
#         '../e2etests/test_data/beans/preprocessing/20190718/metadata.yml').build()
#     with NWBHDF5IO('example_file_path.nwb_builder', mode='r') as io:
#         nwb_file = io.read()
#         print(nwb_file)
