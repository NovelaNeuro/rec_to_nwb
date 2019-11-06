import datetime

import yaml
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject


class MetadataExtractor:

    def __init__(self, path_to_yml='metadata.yml'):
        self.path_to_yml = path_to_yml

        with open("metadata.yml", 'r') as stream:
            try:
                # print(yaml.safe_load(stream))
                metadate_dict = yaml.safe_load(stream)

                self.experimenter_name = metadate_dict['experimenter name']
                self.lab = metadate_dict['lab']
                self.institution = metadate_dict['institution']
                self.experiment_description = metadate_dict['experiment description']
                self.session_description = metadate_dict['session description']
                self.identifier = metadate_dict['identifier']
                self.session_start_time = datetime.datetime.strptime(metadate_dict['session start time'],
                                                                     '%m/%d/%Y %H:%M:%S')
                self.subject = Subject(
                    age=str(metadate_dict['subject']['age']),
                    description=metadate_dict['subject']['description'],
                    genotype=metadate_dict['subject']['genotype'],
                    sex=metadate_dict['subject']['sex'],
                    species=metadate_dict['subject']['species'],
                    subject_id=metadate_dict['subject']['subject id'],
                    weight=str(metadate_dict['subject']['weight']),
                    date_of_birth=datetime.datetime.strptime(metadate_dict['subject']['date of birth'], '%m/%d/%Y')
                )

                # Ciekawostka porownac task= Time().add() z task = Time()  task.add()
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
                    tags=metadate_dict['task']['interval']['tags'],
                    timeseries=metadate_dict['task']['interval']['timeseries'],
                )

                # Used for recording_device, electrodes, location_electrodes
                self.devices = metadate_dict['device']['name']
                self.electrode_groups = metadate_dict['electrode group']
                self.electrodes = metadate_dict['electrode']
            #     ToDo Check if group / device exist if not we create it or raise exception?

            except yaml.YAMLError as exc:
                print(exc)

    def get_experimenter_name(self):
        return self.experimenter_name

    def get_lab(self):
        return self.lab

    def get_institution(self):
        return self.institution

    def get_experiment_description(self):
        return self.experiment_description

    def get_session_description(self):
        return self.session_description

    def get_identifier(self):
        pass

    def get_session_start_time(self):
        return self.session_start_time

    def get_subject(self):
        return self.subject

    def get_task(self):
        return self.task

    def get_devices(self):
        return self.devices

    def get_electrode_groups(self):
        return self.electrode_groups

    def get_electrodes(self):
        return self.electrodes

if __name__ == '__main__':
    obj = MetadataExtractor()
    print(obj.__dict__)
