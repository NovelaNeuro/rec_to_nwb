class IncorrectTypeException(Exception):

    def __init__(self, parameter, parameter_name, expected_type):
        self.parameter = parameter
        self.parameter_name = parameter_name
        self.expected_type = expected_type

    def __str__(self):
        message = 'Parameter ' + str(self.parameter_name) + ' must be type ' + str(self.expected_type)
        return message
