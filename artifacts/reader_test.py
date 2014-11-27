#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import unittest
import os

from artifacts import definitions
from artifacts import reader


class YamlArtifactsReaderTest(unittest.TestCase):
  """Class to test the YAML artifacts reader."""

  def testRead(self):
    """Tests the Read function."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    with open(test_file, 'rb') as file_object:
      artifact_definitions = list(artifact_reader.Read(file_object))

    self.assertEqual(len(artifact_definitions), 5)

    # Artifact with file source type.
    artifact_definition = artifact_definitions[0]
    self.assertEqual(artifact_definition.name, 'SecurityEventLogEvtx')

    expected_description = (
        'Windows Security Event log for Vista or later systems.')
    self.assertEqual(artifact_definition.description, expected_description)
    self.assertEqual(artifact_definition.doc, expected_description)

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertNotEqual(source_type, None)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_FILE)

    expected_locations = sorted([
        '%%environ_systemroot%%\\System32\\winevt\\Logs\\Security.evtx'])
    self.assertEqual(sorted(source_type.locations), expected_locations)

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

    # Artifact with Windows Registry key source type.
    artifact_definition = artifact_definitions[1]
    self.assertEqual(
        artifact_definition.name, 'AllUsersProfileEnvironmentVariable')

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertNotEqual(source_type, None)
    self.assertEqual(
        source_type.type_indicator,
        definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY)

    expected_keys = sorted([
        ('HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
         'ProfileList\\ProfilesDirectory'),
        ('HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
         'ProfileList\\AllUsersProfile')])
    self.assertEqual(sorted(source_type.keys), expected_keys)

    # Artifact with Windows Registry value source type.
    artifact_definition = artifact_definitions[2]
    self.assertEqual(artifact_definition.name, 'CurrentControlSet')

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertNotEqual(source_type, None)
    self.assertEqual(
        source_type.type_indicator,
        definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE)

    expected_key = 'HKEY_LOCAL_MACHINE\\SYSTEM\\Select'
    self.assertEqual(source_type.key, expected_key)
    self.assertEqual(source_type.value, 'Current')

    # Artifact with WMI query source type.
    artifact_definition = artifact_definitions[3]
    self.assertEqual(artifact_definition.name, 'WMIProfileUsersHomeDir')

    expected_provides = sorted(['users.homedir'])
    self.assertEqual(sorted(artifact_definition.provides), expected_provides)

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertNotEqual(source_type, None)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_WMI_QUERY)

    expected_query = (
        'SELECT * FROM Win32_UserProfile WHERE SID=\'%%users.sid%%\'')
    self.assertEqual(source_type.query, expected_query)

    # Artifact with artifact definition source type.
    artifact_definition = artifact_definitions[4]
    self.assertEqual(artifact_definition.name, 'EventLogs')

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertNotEqual(source_type, None)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_ARTIFACT)


if __name__ == '__main__':
  unittest.main()
