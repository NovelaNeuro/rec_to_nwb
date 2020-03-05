from fl.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException


def validate_input_parameters(class_name, *args):
    for arg in args:
        if arg is None:
            raise NoneParamInInitException('None parameter was passed to ' + class_name)
