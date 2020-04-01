from ndx_fllab_novela.nwb_electrode_group import NwbElectrodeGroup

from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodeGroupFactory:

    @classmethod
    def create_nwb_electrode_group(cls, fl_nwb_electrode_group):
        validate_parameters_not_none(__name__, fl_nwb_electrode_group)
        validate_parameters_not_none(__name__, fl_nwb_electrode_group.metadata, fl_nwb_electrode_group.device)
        validate_parameters_not_none(
            class_name=__name__,
            args=[fl_nwb_electrode_group],
            args_name=[NameExtractor.extract_name(cls.create_nwb_electrode_group)[1]]
        )
        validate_parameters_not_none(
            class_name=__name__,
            args=[fl_nwb_electrode_group.metadata, fl_nwb_electrode_group.device],
            args_name=[NameExtractor.extract_name(fl_nwb_electrode_group.__init__)[1]]
        )




        return NwbElectrodeGroup(
            id=fl_nwb_electrode_group.metadata['id'],
            device=fl_nwb_electrode_group.device,
            location=str(fl_nwb_electrode_group.metadata['location']),
            description=str(fl_nwb_electrode_group.metadata['description']),
            name='electrode group ' + str(fl_nwb_electrode_group.metadata["id"])
        )