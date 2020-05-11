import os
import unittest
from pathlib import Path

from testfixtures import should_raise

from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip("NWB file creation")
class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.metadata = MetadataManager(
            str(path) + '/processing/res/metadata.yml',
            [str(path) + '/processing/res/probe1.yml',
             str(path) + '/processing/res/probe2.yml',
             str(path) + '/processing/res/probe3.yml'])

        cls.nwb_builder = NWBFileBuilder(
            data_path=str(path) + '/test_data',
            animal_name='beans',
            date='20190718',
            nwb_metadata=cls.metadata,
            associated_files=[
                (str(path) + '/processing/res/test_text_files/test1_file'),
                (str(path) + '/processing/res/test_text_files/test2_file'),
            ],
            process_dio=True,
            process_mda=True,
            process_analog=True
        )

    def test_generate_nwb(self):
        content = self.nwb_builder.build()
        self.nwb_builder.write(content)
        self.assertIsNotNone(self.nwb_builder)

    @should_raise(TypeError)
    def test_nwb_file_builder_failed_due_to_incorrect_type_of_parameters(self):
        NWBFileBuilder(
            data_path='C:/Users/wbodo/Desktop/resy/test/',
            animal_name='beans',
            date=123,
            nwb_metadata=self.metadata,
            associated_files=[
                (str(path) + '/processing/res/test_text_files/test1_file'),
                (str(path) + '/processing/res/test_text_files/test2_file'),
            ],
            process_dio=True,
            process_mda=True,
            process_analog=True
        )

    @should_raise(TypeError)
    def test_nwb_file_builder_failed_due_to_None_parameter(self):
        NWBFileBuilder(
            data_path='C:/Users/wbodo/Desktop/resy/test/',
            animal_name='beans',
            date=None,
            nwb_metadata=self.metadata,
            associated_files=[
                (str(path) + '/processing/res/test_text_files/test1_file'),
                (str(path) + '/processing/res/test_text_files/test2_file'),
            ],
            process_dio=True,
            process_mda=True,
            process_analog=True
        )

    # @classmethod
    # def tearDownClass(cls):
    #     del cls.nwb_builder
    #     if os.path.isfile('output.nwb'):
    #         os.remove('output.nwb')