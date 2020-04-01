class NoneParamException(Exception):

    def __init__(self, class_name, parameter, parameter_name):
        self.class_name = class_name
        self.parameter_name = parameter_name
        self.parameter = parameter

    def __str__(self):
        message = 'None parameter: ' + str(self.parameter_name) + ' was passed to class: ' + self.class_name
        return message

