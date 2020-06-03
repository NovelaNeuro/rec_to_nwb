from rec_to_nwb.processing.nwb.components.device.fl_probe import FlProbe
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlProbeBuilder:

    @staticmethod
    @beartype
    def build(probe_id: int, name: str, probe_type: str, units: str, probe_description: str,
              contact_side_numbering: bool, contact_size: float, shanks: list):
        return FlProbe(
            probe_id=probe_id,
            name=name,
            probe_type=probe_type,
            units=units,
            probe_description=probe_description,
            contact_side_numbering=contact_side_numbering,
            contact_size=contact_size,
            shanks=shanks
        )
