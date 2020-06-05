from ndx_franklab_novela.probe import Shank

from rec_to_nwb.processing.nwb.components.device.probe.shanks.fl_shank import FlShank
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class ShankCreator:

    @classmethod
    @beartype
    def create(cls, fl_shank: FlShank) -> Shank:
        validate_parameters_not_none(__name__, fl_shank.shank_id, fl_shank.shanks_electrodes)

        shank = Shank(
            name=str(fl_shank.shank_id)
        )
        for shanks_electrode in fl_shank.shanks_electrodes:
            shank.add_shanks_electrode(shanks_electrode)
        return shank
