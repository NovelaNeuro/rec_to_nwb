class NoneParamException(Exception):

    def __init__(self, class_name, parameter):
        self.class_name = class_name
        self.parameter = parameter

    def __str__(self):
        message = 'None parameter passed to class: ' + self.class_name
        return message

