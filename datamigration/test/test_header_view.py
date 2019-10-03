import unittest

from datamigration.datamigration import xml_header_view


class TestHeaderInterface(unittest.TestCase):

    def __init__(self):
        self.header = xml_header_view.XmlHeaderView(filename='fl_lab_sample_header.xml')

    def test_getRoot(self):
        self.assertEqual('Configuration', xml_header_view.XmlHeaderView.getRoot().tag)
        self.assertEqual(None, xml_header_view.XmlHeaderView.getRoot().items())
        self.assertEqual(6, len(xml_header_view.XmlHeaderView.getRoot().getchildren()))


if __name__ == '__main__':
    unittest.main()
