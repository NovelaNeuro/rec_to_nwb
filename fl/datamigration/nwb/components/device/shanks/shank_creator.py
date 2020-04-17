from ndx_fllab_novela.probe import Shank

from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ShankCreator:

    @classmethod
    def create(cls, fl_shank):
        validate_parameters_not_none(__name__, fl_shank)
        validate_parameters_not_none(__name__, fl_shank.shank_id, fl_shank.shanks_electrodes)

        shank = Shank(
            name=fl_shank.shank_id
        )
        for shanks_electrode in fl_shank.shanks_electrodes:
            shank.add_shanks_electrode(shanks_electrode)
        return shank
