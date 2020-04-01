from fl.datamigration.exceptions.not_equal_param_length_exception import NotEqualParamLengthException
from fl.datamigration.exceptions.none_param_exception import NoneParamException


def validate_parameters_not_none(class_name, args, args_name):
    for counter, arg in enumerate(args):
        if arg is None:
            raise NoneParamException(class_name, arg, args_name[counter])


# ToDo Add param_name
def validate_parameters_equal_length(class_name, *args):
    previous_arg = args[0]
    for arg in args:
        if len(arg) != len(previous_arg):
            raise NotEqualParamLengthException('Parameters lengths are not equal in ' + class_name)
        previous_arg = arg
