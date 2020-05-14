from unittest import TestCase
from unittest.mock import Mock

from rec_to_nwb.processing.header.module.header import Header
from rec_to_nwb.processing.tools.dataset import Dataset
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator
from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator


class TestValidationRegistrator(TestCase):

    def test_registers_validators_correctly(self):
        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(NTrodeValidator(dict(), Mock(spec=Header), list()))
        validationRegistrator.register(NTrodeValidator(dict(), Mock(spec=Header), list()))
        self.assertEqual(2, len(validationRegistrator.validators))

    def test_registers_only_validators_correctly(self):
        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(NTrodeValidator(dict(), Mock(spec=Header), list()))
        validationRegistrator.register(None)
        validationRegistrator.register(Dataset(name="name"))

        self.assertEqual(1, len(validationRegistrator.validators))
