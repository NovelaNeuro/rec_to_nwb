import datetime

import yaml
from pynwb.file import Subject


class MetadataExtractor:

    def __init__(self, config_path):
        with open(config_path, 'r') as stream:
            metadata_dict = yaml.safe_load(stream)
            #self.rec_file_link = metadata_dict['rec file link']
            self.experimenter_name = metadata_dict['experimenter name']
            self.lab = metadata_dict['lab']
            self.institution = metadata_dict['institution']
            self.experiment_description = metadata_dict['experiment description']
            self.session_description = metadata_dict['session description']
            self.identifier = metadata_dict['identifier']
            self.session_start_time = datetime.datetime.strptime(metadata_dict['session start time'],
                                                                 '%m/%d/%Y %H:%M:%S')
            #raw_date_of_birth = datetime.datetime.strptime(metadata_dict['subject']['date of birth'], '%m/%d/%Y')
            #timezone = pytz.timezone(metadata_dict['subject']['timezone'])
            #date_of_birth = timezone.localize(raw_date_of_birth)
            self.subject = Subject(
                #age=str(metadata_dict['subject']['age']),
                description=metadata_dict['subject']['description'],
                genotype=metadata_dict['subject']['genotype'],
                sex=metadata_dict['subject']['sex'],
                species=metadata_dict['subject']['species'],
                subject_id=metadata_dict['subject']['subject id'],
                weight=str(metadata_dict['subject']['weight']),
                #date_of_birth=date_of_birth,
            )

            self.tasks = metadata_dict['tasks']

            # self.task = TimeIntervals(
            #     name=metadata_dict['task']['name'],
            #     description=metadata_dict['task']['description'],
            #     id=metadata_dict['task']['id'],
            #     columns=metadata_dict['task']['columns'],
            #     colnames=metadata_dict['task']['colnames'],
            # )

            # self.task.add_interval(
            #     start_time=metadata_dict['task']['interval']['start_time'],
            #     stop_time=metadata_dict['task']['interval']['stop_time'],
            #     tags=str(metadata_dict['task']['interval']['tags']),
            #     timeseries=metadata_dict['task']['interval']['timeseries'],
            # )

            self.devices = metadata_dict['device']['name']
            self.electrode_groups = metadata_dict['electrode group']
            self.electrodes = metadata_dict['electrode']
            self.electrode_regions = metadata_dict['electrode region']
            self.apparatus = metadata_dict['apparatus']['data']
            self.behavioral_event = metadata_dict['behavioral_events']
