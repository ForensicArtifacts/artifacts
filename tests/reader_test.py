# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import os
import unittest

from artifacts import definitions
from artifacts import errors
from artifacts import reader


class YamlArtifactsReaderTest(unittest.TestCase):
  """Class to test the YAML artifacts reader."""

  def testReadFileObject(self):
    """Tests the ReadFileObject function."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    with open(test_file, 'rb') as file_object:
      artifact_definitions = list(artifact_reader.ReadFileObject(file_object))

    self.assertEqual(len(artifact_definitions), 7)

    # Artifact with file source type.
    artifact_definition = artifact_definitions[0]
    self.assertEqual(artifact_definition.name, 'SecurityEventLogEvtx')

    expected_description = (
        'Windows Security Event log for Vista or later systems.')
    self.assertEqual(artifact_definition.description, expected_description)

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertIsNotNone(source_type)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_FILE)

    expected_paths = sorted([
        '%%environ_systemroot%%\\System32\\winevt\\Logs\\Security.evtx'])
    self.assertEqual(sorted(source_type.paths), expected_paths)

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
    self.assertIsNotNone(source_type)
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
    self.assertIsNotNone(source_type)
    self.assertEqual(
        source_type.type_indicator,
        definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE)

    self.assertEqual(len(source_type.key_value_pairs), 1)
    key_value_pair = source_type.key_value_pairs[0]

    expected_key = 'HKEY_LOCAL_MACHINE\\SYSTEM\\Select'
    self.assertEqual(key_value_pair['key'], expected_key)
    self.assertEqual(key_value_pair['value'], 'Current')

    # Artifact with WMI query source type.
    artifact_definition = artifact_definitions[3]
    self.assertEqual(artifact_definition.name, 'WMIProfileUsersHomeDir')

    expected_provides = sorted(['users.homedir'])
    self.assertEqual(sorted(artifact_definition.provides), expected_provides)

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertIsNotNone(source_type)
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
    self.assertIsNotNone(source_type)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_ARTIFACT_GROUP)

    # Artifact with command definition source type.
    artifact_definition = artifact_definitions[5]
    self.assertEqual(artifact_definition.name, 'RedhatPackagesList')

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertIsNotNone(source_type)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_COMMAND)

    # Artifact with COMMAND definition collector definition.
    artifact_definition = artifact_definitions[5]
    self.assertEqual(artifact_definition.name, 'RedhatPackagesList')

    self.assertEqual(len(artifact_definition.sources), 1)
    collector_definition = artifact_definition.sources[0]
    self.assertIsNotNone(collector_definition)
    self.assertEqual(
        collector_definition.type_indicator,
        definitions.TYPE_INDICATOR_COMMAND)

  def testBadKey(self):
    """Tests top level keys are correct."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadKey
doc: bad extra key.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
extra_key: 'wrong'
labels: [Logs]
supported_os: [Windows]
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testMissingSources(self):
    """Tests sources is present."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadSources
doc: must have one sources.
labels: [Logs]
supported_os: [Windows]
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testBadSupportedOS(self):
    """Tests supported_os is checked correctly."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadSupportedOS
doc: supported_os should be an array of strings.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
labels: [Logs]
supported_os: Windows
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testBadLabels(self):
    """Tests labels is checked correctly."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: BadLabel
doc: badlabel.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
labels: Logs
supported_os: [Windows]
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testMissingDoc(self):
    """Tests doc is required."""
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: NoDoc
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testMissingNamesAttribute(self):
    artifact_reader = reader.YamlArtifactsReader()
    file_object = io.StringIO(initial_value=u"""name: NoNames
doc: Missing names attr.
sources:
- type: ARTIFACT_GROUP
  attributes:
    - 'SystemEventLogEvtx'
""")

    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFile(self):
    """Tests the ReadFile function."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))

    self.assertEqual(len(artifact_definitions), 7)

  def testReadDirectory(self):
    """Tests the ReadDirectory function."""
    artifact_reader = reader.YamlArtifactsReader()

    artifact_definitions = list(artifact_reader.ReadDirectory('test_data'))

    self.assertEqual(len(artifact_definitions), 7)


if __name__ == '__main__':
  unittest.main()
