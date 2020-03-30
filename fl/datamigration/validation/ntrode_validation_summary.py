from fl.datamigration.validation.validation_summary import ValidationSummary


class NTrodeValidationSummary(ValidationSummary):

    def __init__(self, ntrodes_num, spike_ntrodes_num):
        self.ntrodes_num = ntrodes_num
        self.spike_ntrodes_num = spike_ntrodes_num

    def isValid(self):
        if (self.ntrodes_num > 0 and self.spike_ntrodes_num > 0 and self.ntrodes_num == self.spike_ntrodes_num):
            return True

        return False
