class IncorrectTypeException(Exception):

    def __init__(self, parameter, expected_type):
        self.parameter = parameter
        self.expected_type = expected_type

    def __str__(self):
        message = 'Parameter ' + str(self.parameter) + ' must be type ' + str(self.expected_type)
        return message
