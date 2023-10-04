from pynwb import NWBFile
from rec_to_nwb.processing.nwb.components.electrodes.fl_electrodes import \
    FlElectrode
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import \
    validate_parameters_not_none


class ElectrodesCreator:

    @classmethod
    @beartype
    def create(cls, nwb_content: NWBFile, fl_electrode: FlElectrode):
        validate_parameters_not_none(
            __name__, fl_electrode.electrode_group, fl_electrode.electrode_id)

        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=fl_electrode.electrode_group,
            id=fl_electrode.electrode_id
        )
