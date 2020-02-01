from src.datamigration.extension.probe import Probe


class DeviceCreator:  # todo isn't it ProbeFactory? why counter instead of id?
    @staticmethod
    def create_device(probe_metadata, device_counter):
        return Probe(
                probe_type=probe_metadata["probe_type"],
                contact_size=probe_metadata["contact_size"],
                num_shanks=probe_metadata['num_shanks'],
                id=device_counter,
                name=str(device_counter)
            )


