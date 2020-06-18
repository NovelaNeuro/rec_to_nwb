import os
from datetime import datetime
from unittest.mock import Mock

from dateutil.tz import tzlocal
from hdmf.common.table import VectorData
from pynwb import NWBFile, ProcessingModule, NWBHDF5IO
from pynwb.testing import TestCase

from rec_to_nwb.processing.nwb.components.task.fl_task import FlTask
from rec_to_nwb.processing.nwb.components.task.task_creator import TaskCreator


class TestTaskIntegration(TestCase):

    def test_task_creator_create_task_and_write_to_nwb_successfully(self):
        nwb_content = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )
        processing_module = ProcessingModule('pm', 'none')

        mock_fl_task_0 = Mock(spec=FlTask)
        mock_fl_task_0.name = 'task_0'
        mock_fl_task_0.description = ''
        mock_fl_task_0.columns = [
            VectorData(
                name='task_name',
                description='',
                data=['Sleep']
            ),
            VectorData(
                name='task_description',
                description='',
                data=['The animal sleeps in a small empty box.']
            ),
            VectorData(
                name='camera_id',
                description='',
                data=[[0]]
            ),
            VectorData(
                name='task_epochs',
                description='',
                data=[[1, 3, 5]]
            ),
        ]
        mock_fl_task_1 = Mock(spec=FlTask)
        mock_fl_task_1.name = 'task_1'
        mock_fl_task_1.description = ''
        mock_fl_task_1.columns = [
            VectorData(
                name='task_name',
                description='',
                data=['Stem+Leaf']
            ),
            VectorData(
                name='task_description',
                description='',
                data=['Spatial Bandit']
            ),
            VectorData(
                name='camera_id',
                description='',
                data=[[1, 2]]
            ),
            VectorData(
                name='task_epochs',
                description='',
                data=[[2, 4]]
            ),
        ]

        task_0 = TaskCreator.create(mock_fl_task_0)
        task_1 = TaskCreator.create(mock_fl_task_1)

        processing_module.add(task_0)
        processing_module.add(task_1)
        nwb_content.add_processing_module(processing_module)

        with NWBHDF5IO(path='task.nwb', mode='w') as nwb_file_io:
            nwb_file_io.write(nwb_content)
            nwb_file_io.close()

        with NWBHDF5IO(path='task.nwb', mode='r') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            self.assertContainerEqual(nwb_content.processing['pm'].data_interfaces['task_0'], task_0)
            self.assertContainerEqual(nwb_content.processing['pm'].data_interfaces['task_1'], task_1)

        os.remove('task.nwb')
