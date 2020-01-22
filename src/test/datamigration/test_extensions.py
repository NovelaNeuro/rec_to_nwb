import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.extension.apparatus import Apparatus
from src.datamigration.extension.edge import Edge
from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.node import Node
from src.datamigration.extension.ntrode import NTrode
from src.datamigration.extension.probe import Probe


class TestExtensions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        cls.probe = Probe(
            name='Probe1',
            id=1,
            probe_type='some type',
            contact_size=20.0,
            num_shanks=2,
        )
        cls.nwb_file.add_device(cls.probe)

        cls.fl_electrode_group = FLElectrodeGroup(
            name='FLElectrodeGroup1',
            description='sample description',
            location='sample location',
            device=cls.probe,
            id=1,
            probe_id=1
        )
        cls.nwb_file.add_electrode_group(cls.fl_electrode_group)

        cls.n_trode = NTrode(
            name='NTrode1',
            description='sample description',
            location='sample location',
            device=cls.probe,
            probe_id=1,
            ntrode_id=1,
            map=[[0, 0], [1, 1], [2, 2]]
        )
        cls.nwb_file.add_electrode_group(cls.n_trode)

        cls.node11 = Node(
            name='1',
            value=0
        )
        cls.node12 = Node(
            name='2',
            value=0
        )
        cls.node13 = Node(
            name='3',
            value=0
        )
        cls.node21 = Node(
            name='4',
            value=1
        )
        cls.node22 = Node(
            name='5',
            value=1
        )
        cls.node23 = Node(
            name='6',
            value=1
        )

        cls.edge1 = Edge(
            name='edge1',
            edge_nodes=[
                cls.node11, cls.node12, cls.node13
            ]
        )

        cls.edge2 = Edge(
            name='edge2',
            edge_nodes=[
                cls.node21, cls.node22, cls.node23
            ]
        )

        cls.apparatus = Apparatus(
            name='Apparatus1',
            edges=[cls.edge1, cls.edge2],
            nodes=[cls.node11, cls.node12, cls.node13, cls.node21, cls.node22, cls.node23]
        )

        cls.nwb_file.create_processing_module(
            name='apparatus',
            description=''
        ).add_data_interface(
            cls.apparatus
        )

    def test_probe_creation(self):
        return_probe = self.nwb_file.get_device(name='Probe1')

        self.assertEqual(self.probe, return_probe)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.id, return_probe.id)
        self.assertEqual(self.probe.contact_size, return_probe.contact_size)
        self.assertEqual(self.probe.num_shanks, return_probe.num_shanks)

    def test_fl_electrode_group_creation(self):
        return_fl_electrode_group = self.nwb_file.get_electrode_group(name='FLElectrodeGroup1')

        self.assertEqual(self.fl_electrode_group, return_fl_electrode_group)
        self.assertEqual(self.fl_electrode_group.name, return_fl_electrode_group.name)
        self.assertEqual(self.fl_electrode_group.description, return_fl_electrode_group.description)
        self.assertEqual(self.fl_electrode_group.location, return_fl_electrode_group.location)
        self.assertEqual(self.fl_electrode_group.device, return_fl_electrode_group.device)
        self.assertEqual(self.fl_electrode_group.probe_id, return_fl_electrode_group.probe_id)
        self.assertEqual(self.fl_electrode_group.id, return_fl_electrode_group.id)

    def test_n_trode_creation(self):
        return_n_trode = self.nwb_file.get_electrode_group(name='NTrode1')

        self.assertEqual(self.n_trode, return_n_trode)
        self.assertEqual(self.n_trode.name, return_n_trode.name)
        self.assertEqual(self.n_trode.description, return_n_trode.description)
        self.assertEqual(self.n_trode.location, return_n_trode.location)
        self.assertEqual(self.n_trode.device, return_n_trode.device)
        self.assertEqual(self.n_trode.probe_id, return_n_trode.probe_id)
        self.assertEqual(self.n_trode.ntrode_id, return_n_trode.ntrode_id)
        self.assertEqual(self.n_trode.map, return_n_trode.map)

    def test_apparatus_creation(self):
        return_apparatus = self.nwb_file.processing['apparatus']['Apparatus1']

        self.assertEqual(self.apparatus, return_apparatus)
        self.assertEqual(self.apparatus.name, return_apparatus.name)
        self.assertEqual(self.apparatus.edges, return_apparatus.edges)
        self.assertEqual(self.apparatus.nodes, return_apparatus.nodes)


