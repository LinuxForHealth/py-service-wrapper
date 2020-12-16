import unittest

from ..utils import yaml_parser

class TestYamlParser(unittest.TestCase):
    def test_parse_project_configuration(self):
        project_file = yaml_parser._parse_project_configuration('webwrapper/tests/resources/test_sync_project_file.yaml')
        self.assertIsNotNone(project_file)
        self.assertIsNotNone(project_file['project'])
        self.assertIsNotNone(project_file['project']['name'])
        self.assertEqual(project_file['project']['name'], 'thisIsMyProject')

    def test_get_project_configuration(self):
        project_file = yaml_parser.get_project_configuration(project_root = 'webwrapper/tests/resources', project_filename='test_async_project_file.yaml')
        self.assertIsNotNone(project_file)
        self.assertIsNotNone(project_file['project'])
        self.assertIsNotNone(project_file['project']['name'])
        self.assertEqual(project_file['project']['name'], 'thisIsMyProject')
        self.assertEqual(project_file['async'], True)

        with self.assertRaises(ValueError) as ex_check:
            yaml_parser.get_project_configuration('webwrapper/tests/resources', 'project.yaml')
        self.assertEqual(str(ex_check.exception), 'webwrapper/tests/resources/project.yaml does not exist in the project root')

        with self.assertRaises(ValueError) as ex_check:
            yaml_parser.get_project_configuration('webwrapper/tests', 'resources')
        self.assertEqual(str(ex_check.exception), 'webwrapper/tests/resources is not a file')

    def test_is_project_async(self):
        