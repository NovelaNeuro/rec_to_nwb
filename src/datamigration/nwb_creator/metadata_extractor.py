import datetime

import yaml
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject


class MetadataExtractor:

    def __init__(self, path_to_yml='./nwb_creator/metadata.yml'):
        self.path_to_yml = path_to_yml
        with open(path_to_yml, 'r') as stream:
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

            # self.task.add_interval(
            #     start_time=metadate_dict['task']['interval']['start_time'],
            #     stop_time=metadate_dict['task']['interval']['stop_time'],
            #     tags=metadate_dict['task']['interval']['tags'],
            #     timeseries=metadate_dict['task']['interval']['timeseries'],
            # )

            # Used for recording_device, electrodes, location_electrodes
            self.devices = metadate_dict['device']['name']
            self.electrode_groups = metadate_dict['electrode group']
            self.electrodes = metadate_dict['electrode']
            self.electrode_regions = metadate_dict['electrode region']
        #     ToDo Check if group / device exist if not we create it or raise exception?


if __name__ == '__main__':
    obj = MetadataExtractor()
    print(obj.lab)
