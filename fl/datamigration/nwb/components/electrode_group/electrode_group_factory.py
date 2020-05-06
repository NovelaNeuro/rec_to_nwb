from ndx_fl_novela.nwb_electrode_group import NwbElectrodeGroup
from pynwb.ecephys import ElectrodeGroup

from fl.datamigration.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup
from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from fl.datamigration.tools.beartype.beartype import beartype
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodeGroupFactory:

    @classmethod
    @beartype
    def create_electrode_group(cls, fl_electrode_group: FlElectrodeGroup):
        validate_parameters_not_none(__name__, fl_electrode_group.name, fl_electrode_group.description,
                                     fl_electrode_group.location, fl_electrode_group.device)

        return ElectrodeGroup(
            name=fl_electrode_group.name,
            description=fl_electrode_group.description,
            location=fl_electrode_group.location,
            device=fl_electrode_group.device,
        )

    @classmethod
    @beartype
    def create_nwb_electrode_group(cls, fl_nwb_electrode_group: FlNwbElectrodeGroup):
        validate_parameters_not_none(__name__, fl_nwb_electrode_group.name, fl_nwb_electrode_group.description,
                                     fl_nwb_electrode_group.location, fl_nwb_electrode_group.device,
                                     fl_nwb_electrode_group.targeted_location,
                                     fl_nwb_electrode_group.targeted_x, fl_nwb_electrode_group.targeted_y,
                                     fl_nwb_electrode_group.targeted_z,
                                     fl_nwb_electrode_group.units
                                     )
        return NwbElectrodeGroup(
            name=fl_nwb_electrode_group.name,
            description=fl_nwb_electrode_group.description,
            location=fl_nwb_electrode_group.location,
            device=fl_nwb_electrode_group.device,
            targeted_location=fl_nwb_electrode_group.targeted_location,
            targeted_x=fl_nwb_electrode_group.targeted_x,
            targeted_y=fl_nwb_electrode_group.targeted_y,
            targeted_z=fl_nwb_electrode_group.targeted_z,
            units=fl_nwb_electrode_group.units,
        )
