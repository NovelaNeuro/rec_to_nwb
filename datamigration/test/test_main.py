import unittest


class TestHeaderView(unittest.TestCase):

    # beforeClass -
    def __init__(self):
        header = datamigration.RECHeader(pathTo_fl_lab_xml_file)

    # --------------------
    def test_get_configuration(self):
        ElementTree
        configuration = header.getConfiguration()
        self.assertEqual('Configuration', root.getName())

    def test_get_global_configuration(self):
        ElementTree
        element = header.getGlobalConfiguration()
        GlobalConfiguration
        globalConfiguration = datamigration.GlobalConfiguration(element)
        self.assertEqual('GlobalConfiguration', globalConfiguration.getName())
        self.assertEqual('1234 56', globalConfiguration.getHeadstageSerial())

    # --------------------


    def test_get_tree(self):
        self.assertEqual('xml.etree.ElementTree.ElementTree', test.get_tree())

    def test_get_root(self):
        self.assertEqual('Configuration', test.get_root().tag)

    def test_get_element(self):
        self.assertEqual('GlobalConfiguration', test.get_element('GlobalConfiguration').tag)
        self.assertEqual(None, test.get_element('SomeTestThing'))

    def test_get_elements(self):
        self.assertEqual(4, len(test.get_elements('Device')))
        self.assertEqual(1, test.get_elements('Device')[1].get('numBytes'))

    def test_get_internal_elements(self):
        self.assertEqual('Device', test.get_internal_elements('HardwareConfiguration')[2].tag)

    def test_get_element_specification(self):
        self.assertEqual(0, test.get_element_specification('GlobalConfiguration')['headstageSmartRefOn'])
        self.assertEqual(None, test.get_element_specification('Configuration'))


