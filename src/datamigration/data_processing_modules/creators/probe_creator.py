from src.datamigration.extension.probe import Probe


class ProbeCreator:  # todo isn't it ProbeFactory?
    @staticmethod
    def create_probe(probe_metadata, probe_id):
        return Probe(
                probe_type=probe_metadata['probe_type'],
                contact_size=probe_metadata['contact_size'],
                num_shanks=probe_metadata['num_shanks'],
                id=probe_id,
                name=str(probe_id)
            )


