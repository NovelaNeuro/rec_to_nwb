from fl.datamigration.exceptions.invalid_exception import InvalidException


class InvalidMetadataException(InvalidException):

    def __str__(self):
        if self.message:
            return 'InvalidMetadataException, {0} '.format(self.message)
        else:
            return 'InvalidMetadataException has been trown!'
