# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import unittest
import os

from artifacts import definitions
from artifacts import errors
from artifacts import reader


class YamlArtifactsReadertest(unittest.TestCase):
  """Class to test the YAML artifacts reader."""

  def testRead(self):
    """Tests the Read function."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    with open(test_file, 'rb') as file_object:
      artifact_definitions = list(artifact_reader.Read(file_object))

    self.assertEqual(len(artifact_definitions), 7)

    # Artifact with file collector definition.
    artifact_definition = artifact_definitions[0]
    self.assertEqual(artifact_definition.name, 'SecurityEventLogEvtx')

    expected_description = (
        'Windows Security Event log for Vista or later systems.')
    self.assertEqual(artifact_definition.description, expected_description)
    self.assertEqual(artifact_definition.doc, expected_description)

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator, definitions.TYPE_INDICATOR_FILE)

    expected_path_list = sorted([
        '%%environ_systemroot%%\\System32\\winevt\\Logs\\Security.evtx'])
    self.assertEqual(sorted(collector_definition.path_list), expected_path_list)

    self.assertEqual(len(artifact_definition.conditions), 1)
    expected_condition = 'os_major_version >= 6'
    self.assertEqual(artifact_definition.conditions[0], expected_condition)

    self.assertEqual(len(artifact_definition.labels), 1)
    self.assertEqual(artifact_definition.labels[0], 'Logs')

    self.assertEqual(len(artifact_definition.supported_os), 1)
    self.assertEqual(artifact_definition.supported_os[0], 'Windows')

    self.assertEqual(len(artifact_definition.urls), 1)
    expected_url = (
        'http://www.forensicswiki.org/wiki/Windows_XML_Event_Log_(EVTX)')
    self.assertEqual(artifact_definition.urls[0], expected_url)

    # Artifact with Windows Registry key collector definition.
    artifact_definition = artifact_definitions[1]
    self.assertEqual(
        artifact_definition.name, 'AllUsersProfileEnvironmentVariable')

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY)

    expected_path_list = sorted([
        ('HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
         'ProfileList\\ProfilesDirectory'),
        ('HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
         'ProfileList\\AllUsersProfile')])
    self.assertEqual(sorted(collector_definition.path_list), expected_path_list)

    # Artifact with Windows Registry value collector definition.
    artifact_definition = artifact_definitions[2]
    self.assertEqual(artifact_definition.name, 'CurrentControlSet')

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE)

    expected_path_list = sorted([
        'HKEY_LOCAL_MACHINE\\SYSTEM\\Select\\Current'])
    self.assertEqual(sorted(collector_definition.path_list), expected_path_list)

    # Artifact with WMI query collector definition.
    artifact_definition = artifact_definitions[3]
    self.assertEqual(artifact_definition.name, 'WMIProfileUsersHomeDir')

    expected_provides = sorted(['users.homedir'])
    self.assertEqual(sorted(artifact_definition.provides), expected_provides)

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_WMI_QUERY)

    expected_query = (
        'SELECT * FROM Win32_UserProfile WHERE SID=\'%%users.sid%%\'')
    self.assertEqual(collector_definition.query, expected_query)

    # Artifact with artifact definition collector definition.
    artifact_definition = artifact_definitions[4]
    self.assertEqual(artifact_definition.name, 'EventLogs')

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_ARTIFACT)

    # Artifact with COMMAND definition collector definition.
    artifact_definition = artifact_definitions[5]
    self.assertEqual(artifact_definition.name, 'RedhatPackagesList')

    self.assertEqual(len(artifact_definition.collectors), 1)
    collector_definition = artifact_definition.collectors[0]
    self.assertNotEqual(collector_definition, None)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_COMMAND)

  def testBadSupportedOS(self):
    """Tests supported_os is checked correctly."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadSupportedOS
doc: supported_os should be an array of strings.
collectors:
- collector_type: ARTIFACT
  args:
    artifact_list:
      - 'SystemEventLogEvtx'
labels: [Logs]
supported_os: Windows
""")

    with self.assertRaises(errors.FormatError):
      artifact_definitions = list(artifact_reader.Read(file_object))

  def testBadLabels(self):
    """Tests labels is checked correctly."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadLabel
doc: badlabel.
collectors:
- collector_type: ARTIFACT
  args:
    artifact_list:
      - 'SystemEventLogEvtx'
labels: Logs
supported_os: [Windows]
""")

    with self.assertRaises(errors.FormatError):
      artifact_definitions = list(artifact_reader.Read(file_object))

  def testMissingDoc(self):
    """Tests doc is required."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: NoDoc
collectors:
- collector_type: ARTIFACT
  args:
    artifact_list:
      - 'SystemEventLogEvtx'
""")

    with self.assertRaises(errors.FormatError):
      artifact_definitions = list(artifact_reader.Read(file_object))


if __name__ == '__main__':
  unittest.main()
