from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException


class MetadataSectionValidator:

    def __init__(self, metadata):
        self.metadata = metadata

    def validate_sections(self):
        if 'experimenter_name' not in self.metadata:
            raise MissingDataException('metadata is missing experimenter_name')
        if 'lab' not in self.metadata:
            raise MissingDataException('metadata is missing lab')
        if 'institution' not in self.metadata:
            raise MissingDataException('metadata is missing institution')
        if 'experiment description' not in self.metadata:
            raise MissingDataException('metadata is missing experiment description')
        if 'session description' not in self.metadata:
            raise MissingDataException('metadata is missing session description')
        if 'session_id' not in self.metadata:
            raise MissingDataException('metadata is missing session_id')
        if 'subject' not in self.metadata:
            raise MissingDataException('metadata is missing subject')
        if 'units' not in self.metadata:
            raise MissingDataException('metadata is missing units')
        if 'data acq device' not in self.metadata:
            raise MissingDataException('metadata is missing data acq device')
        if 'cameras' not in self.metadata:
            raise MissingDataException('metadata is missing cameras')
        if 'tasks' not in self.metadata:
            raise MissingDataException('metadata is missing tasks')
        if 'associated_files' not in self.metadata:
            raise MissingDataException('metadata is missing associated_files')
        if 'associated_video_files' not in self.metadata:
            raise MissingDataException('metadata is missing associated_video_files')
        if 'times_period_multiplier' not in self.metadata:
            raise MissingDataException('metadata is missing times_period_multiplier')
        if 'behavioral_events' not in self.metadata:
            raise MissingDataException('metadata is missing behavioral_events')
        if 'electrode groups' not in self.metadata:
            raise MissingDataException('metadata is missing electrode groups')
        if 'ntrode electrode group channel map' not in self.metadata:
            raise MissingDataException('metadata is missing ntrode electrode group channel map')
