from rec_to_nwb.processing.exceptions.missing_data_exception import \
    MissingDataException


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
        if 'experiment_description' not in self.metadata:
            raise MissingDataException(
                'metadata is missing experiment_description')
        if 'session_description' not in self.metadata:
            raise MissingDataException(
                'metadata is missing session_description')
        if 'session_id' not in self.metadata:
            raise MissingDataException('metadata is missing session_id')
        if 'subject' not in self.metadata:
            raise MissingDataException('metadata is missing subject')
        if 'units' not in self.metadata:
            raise MissingDataException('metadata is missing units')
        if 'data_acq_device' not in self.metadata:
            raise MissingDataException('metadata is missing data_acq_device')
        if 'cameras' not in self.metadata:
            raise MissingDataException('metadata is missing cameras')
        if 'tasks' not in self.metadata:
            raise MissingDataException('metadata is missing tasks')
        if 'associated_files' not in self.metadata:
            raise MissingDataException('metadata is missing associated_files')
        if 'associated_video_files' not in self.metadata:
            raise MissingDataException(
                'metadata is missing associated_video_files')
        if 'times_period_multiplier' not in self.metadata:
            raise MissingDataException(
                'metadata is missing times_period_multiplier')
        if 'behavioral_events' not in self.metadata:
            raise MissingDataException('metadata is missing behavioral_events')
        if 'electrode_groups' not in self.metadata:
            raise MissingDataException('metadata is missing electrode_groups')
        if 'ntrode_electrode_group_channel_map' not in self.metadata:
            raise MissingDataException(
                'metadata is missing ntrode_electrode_group_channel_map')
