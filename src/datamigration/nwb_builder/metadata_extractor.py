import datetime

import pytz
import yaml
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject


class MetadataExtractor:

    def __init__(self, configuration_path='metadata.yml'):
        self.configuration_path = configuration_path
        with open(self.configuration_path, 'r') as stream:
            metadate_dict = yaml.safe_load(stream)
            self.experimenter_name = metadate_dict['experimenter name']
            self.lab = metadate_dict['lab']
            self.institution = metadate_dict['institution']
            self.experiment_description = metadate_dict['experiment description']
            self.session_description = metadate_dict['session description']
            self.identifier = metadate_dict['identifier']
            self.session_start_time = datetime.datetime.strptime(metadate_dict['session start time'],
                                                                 '%m/%d/%Y %H:%M:%S')
            raw_date_of_birth = datetime.datetime.strptime(metadate_dict['subject']['date of birth'], '%m/%d/%Y')
            timezone = pytz.timezone(metadate_dict['subject']['timezone'])
            date_of_birth = timezone.localize(raw_date_of_birth)
            self.subject = Subject(
                age=str(metadate_dict['subject']['age']),
                description=metadate_dict['subject']['description'],
                genotype=metadate_dict['subject']['genotype'],
                sex=metadate_dict['subject']['sex'],
                species=metadate_dict['subject']['species'],
                subject_id=metadate_dict['subject']['subject id'],
                weight=str(metadate_dict['subject']['weight']),
                date_of_birth=date_of_birth
            )

            self.task = TimeIntervals(
                name=metadate_dict['task']['name'],
                description=metadate_dict['task']['description'],
                id=metadate_dict['task']['id'],
                columns=metadate_dict['task']['columns'],
                colnames=metadate_dict['task']['colnames'],
            )

            self.task.add_interval(
                start_time=metadate_dict['task']['interval']['start_time'],
                stop_time=metadate_dict['task']['interval']['stop_time'],
                tags=str(metadate_dict['task']['interval']['tags']),
                timeseries=metadate_dict['task']['interval']['timeseries'],
            )

            self.devices = metadate_dict['device']['name']
            self.electrode_groups = metadate_dict['electrode group']
            self.electrodes = metadate_dict['electrode']
            self.electrode_regions = metadate_dict['electrode region']
