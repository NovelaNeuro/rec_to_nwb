from rec_to_nwb.processing.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException


def validate_parameters_not_none(class_name, *args):
    for arg in args:
        if arg is None:
            raise NoneParamException('None parameter passed to ' + class_name)


def validate_parameters_equal_length(class_name, *args):
    previous_arg = args[0]
    for arg in args:
        if len(arg) != len(previous_arg):
            raise NotEqualParamLengthException('Parameters lengths are not equal in ' + class_name)
        previous_arg = arg
