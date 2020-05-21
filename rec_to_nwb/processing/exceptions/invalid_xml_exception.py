from rec_to_nwb.processing.exceptions.invalid_exception import InvalidException


class InvalidXMLException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidXMLException, {0} '.format(self.message)
        return 'InvalidHeaderException has been thrown!'

