from unittest import TestCase
from unittest.mock import Mock

from fl.datamigration.tools.dataset import Dataset
from fl.datamigration.tools.task_validator import TaskValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator
from fl.datamigration.validation.ntrode_validator import NTrodeValidator
from fl.datamigration.validation.ntrode_validation_summary import NTrodeValidationSummary
from fl.datamigration.validation.validator import Validator


class TestValidationRegistrator(TestCase):

    def test_registers_validators_correctly(self):
        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(NTrodeValidator(None, None))
        validationRegistrator.register(NTrodeValidator(None, None))
        self.assertEqual(2, len(validationRegistrator.validators))

    def test_registers_only_validators_correctly(self):
        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(NTrodeValidator(None, None))
        validationRegistrator.register(None)
        validationRegistrator.register(Dataset(name="name"))

        self.assertEqual(1, len(validationRegistrator.validators))
