from unittest import TestCase

from rec_to_nwb.processing.tools.dataset import Dataset
from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator


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
