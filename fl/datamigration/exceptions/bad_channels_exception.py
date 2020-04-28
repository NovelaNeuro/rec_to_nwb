from fl.datamigration.exceptions.invalid_exception import InvalidException


class BadChannelsException(InvalidException):

    def __str__(self):
        if self.message:
            return 'BadChannelsException, {0} '.format(self.message)
        else:
            return 'BadChannelsException has been thrown!'
