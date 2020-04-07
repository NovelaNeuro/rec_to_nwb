import unittest
from datetime import datetime
from pathlib import Path

from dateutil.tz import tzlocal
from pynwb import NWBFile, ProcessingModule
from pynwb.behavior import BehavioralEvents

from fl.datamigration.nwb.components.dio.dio_injector import DioInjector

path = Path(__file__).parent.parent
path.resolve()

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())


class TestDioManager(unittest.TestCase):

    def setUp(self):
        self.nwb_content = NWBFile(
            session_description='session description',
            experimenter='experimenter name',
            lab='lab',
            institution='institution',
            session_start_time=start_time,
            identifier='identifier',
            experiment_description='experiment description')

        processing_module = ProcessingModule(name='test_processing_module_name', description='test_description')
        self.nwb_content.add_processing_module(processing_module)
        self.behavioral_events = BehavioralEvents(name='test_BehavioralEvents_name')

        self.dio_injector = DioInjector(self.nwb_content)

    def test_dio_injector(self):
        self.dio_injector.inject(
            self.behavioral_events,
            processing_module_name='test_processing_module_name')
        self.assertEqual(self.behavioral_events,
                         self.nwb_content.processing['test_processing_module_name']['test_BehavioralEvents_name'])
