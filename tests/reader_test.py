# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import unittest
import yaml

from artifacts import definitions
from artifacts import errors
from artifacts import reader

from tests import test_lib


class YamlArtifactsReaderTest(test_lib.BaseTestCase):
  """YAML artifacts reader tests."""

  _DEFINITION_INVALID_SUPPORTED_OS_1 = """\
name: BadSupportedOS
doc: supported_os should be an array of strings.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
supported_os: Windows
"""

  _DEFINITION_INVALID_SUPPORTED_OS_2 = """\
name: BadTopSupportedOS
doc: Top supported_os should match supported_os from sources.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
  supported_os: [Windows]
"""

  _DEFINITION_INVALID_URLS = """\
name: BadUrls
doc: badurls.
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
supported_os: [Windows]
urls: 'http://example.com'
"""

  _DEFINITION_WITH_EXTRA_KEY = """\
name: WithExtraKey
doc: definition with extra_key
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
extra_key: 'wrong'
supported_os: [Windows]
"""

  _DEFINITION_WITH_RETURN_TYPES = """\
name: WithReturnTypes
doc: definition with return_types
sources:
- type: ARTIFACT_GROUP
  attributes:
    names: [WindowsRunKeys, WindowsServices]
  returned_types: [PersistenceFile]
"""

  _DEFINITION_WITHOUT_DOC = """\
name: NoDoc
sources:
- type: ARTIFACT_GROUP
  attributes:
    names:
      - 'SystemEventLogEvtx'
"""

  _DEFINITION_WITHOUT_NAME = """\
name: NoNames
doc: Missing names attr.
sources:
- type: ARTIFACT_GROUP
  attributes:
    - 'SystemEventLogEvtx'
"""

  _DEFINITION_WITHOUT_SOURCES = """\
name: BadSources
doc: must have one sources.
supported_os: [Windows]
"""

  def testReadFileObject(self):
    """Tests the ReadFileObject function."""
    test_file = self._GetTestFilePath(['definitions.yaml'])
    self._SkipIfPathNotExists(test_file)

    artifact_reader = reader.YamlArtifactsReader()

    with open(test_file, 'rb') as file_object:
      artifact_definitions = list(artifact_reader.ReadFileObject(file_object))

    self.assertEqual(len(artifact_definitions), 7)

    # Artifact with file source type.
    artifact_definition = artifact_definitions[0]
    self.assertEqual(artifact_definition.name, 'SecurityEventLogEvtxFile')

    expected_description = (
        'Windows Security Event log for Vista or later systems.')
    self.assertEqual(artifact_definition.description, expected_description)

    self.assertEqual(len(artifact_definition.sources), 1)
    source_type = artifact_definition.sources[0]
    self.assertIsNotNone(source_type)
    self.assertEqual(
        source_type.type_indicator, definitions.TYPE_INDICATOR_FILE)

    expected_paths = [
        '%%environ_systemroot%%\\System32\\winevt\\Logs\\Security.evtx'
    ]
    self.assertEqual(sorted(source_type.paths), sorted(expected_paths))

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

    expected_key1 = (
        'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
        'ProfileList\\ProfilesDirectory')
    expected_key2 = (
        'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
        'ProfileList\\AllUsersProfile')
    expected_keys = [expected_key1, expected_key2]

    self.assertEqual(sorted(source_type.keys), sorted(expected_keys))

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
        collector_definition.type_indicator, definitions.TYPE_INDICATOR_COMMAND)

  def testReadFileObjectInvalidSupportedOS(self):
    """Tests the ReadFileObject function on an invalid supported_os."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(
        initial_value=self._DEFINITION_INVALID_SUPPORTED_OS_1)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

    file_object = io.StringIO(
        initial_value=self._DEFINITION_INVALID_SUPPORTED_OS_2)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectInvalidURLs(self):
    """Tests the ReadFileObject function on an invalid urls."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_INVALID_URLS)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectWithExtraKey(self):
    """Tests the ReadFileObject function on a definition with extra key."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_WITH_EXTRA_KEY)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectWithReturnTypes(self):
    """Tests the ReadFileObject function on a definition with return types."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_WITH_RETURN_TYPES)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectWithoutDoc(self):
    """Tests the ReadFileObject function on a definition without doc."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_WITHOUT_DOC)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectWithoutName(self):
    """Tests the ReadFileObject function on a definition without name."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_WITHOUT_NAME)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadFileObjectWithoutSources(self):
    """Tests the ReadFileObject function on a definition without sources."""
    artifact_reader = reader.YamlArtifactsReader()

    file_object = io.StringIO(initial_value=self._DEFINITION_WITHOUT_SOURCES)
    with self.assertRaises(errors.FormatError):
      _ = list(artifact_reader.ReadFileObject(file_object))

  def testReadYamlFile(self):
    """Tests the ReadFile function."""
    test_file = self._GetTestFilePath(['definitions.yaml'])
    self._SkipIfPathNotExists(test_file)

    artifact_reader = reader.YamlArtifactsReader()

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    self.assertEqual(len(artifact_definitions), 7)

  def testReadDirectory(self):
    """Tests the ReadDirectory function."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = self._GetTestFilePath(['.'])

    artifact_definitions = list(artifact_reader.ReadDirectory(test_file))
    self.assertEqual(len(artifact_definitions), 7)

  def testArtifactAsDict(self):
    """Tests the AsDict function."""
    test_file = self._GetTestFilePath(['definitions.yaml'])
    self._SkipIfPathNotExists(test_file)

    artifact_reader = reader.YamlArtifactsReader()

    with open(test_file, 'r', encoding='utf-8') as file_object:
      for artifact_definition in yaml.safe_load_all(file_object):
        artifact_object = artifact_reader.ReadArtifactDefinitionValues(
            artifact_definition)
        self.assertEqual(artifact_definition, artifact_object.AsDict())

  def testDefinitionsAsDict(self):
    """Tests the AsDict function."""
    artifact_reader = reader.YamlArtifactsReader()

    artifact_definitions = list(artifact_reader.ReadDirectory('data'))

    last_artifact_definition = None
    for artifact in artifact_definitions:
      try:
        artifact_definition = artifact.AsDict()
      except errors.FormatError:
        error_location = 'At start'
        if last_artifact_definition:
          error_location = f'After: {last_artifact_definition.name:s}'
        self.fail(f'{error_location:s} failed to convert to dict')
      last_artifact_definition = artifact_definition


class JsonArtifactsReaderTest(test_lib.BaseTestCase):
  """JSON artifacts reader tests."""

  def testReadJsonFile(self):
    """Tests the ReadFile function."""
    test_file = self._GetTestFilePath(['definitions.json'])
    self._SkipIfPathNotExists(test_file)

    artifact_reader = reader.JsonArtifactsReader()

    artifact_definitions = list(artifact_reader.ReadFile(test_file))

    self.assertEqual(len(artifact_definitions), 7)


if __name__ == '__main__':
  unittest.main()
