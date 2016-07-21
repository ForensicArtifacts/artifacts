# -*- coding: utf-8 -*-
"""Tests for the artifact definitions registry."""

import io
import os
import unittest

from artifacts import errors
from artifacts import reader
from artifacts import registry


class ArtifactDefinitionsRegistryTest(unittest.TestCase):
  """Tests for the artifact definitions registry."""

  def testArtifactDefinitionsRegistry(self):
    """Tests the ArtifactDefinitionsRegistry functions."""
    artifact_registry = registry.ArtifactDefinitionsRegistry()

    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join(u'test_data', u'definitions.yaml')

    for artifact_definition in artifact_reader.ReadFile(test_file):
      artifact_registry.RegisterDefinition(artifact_definition)

    # Make sure the test file got turned into artifacts.
    self.assertEqual(len(artifact_registry.GetDefinitions()), 7)

    artifact_definition = artifact_registry.GetDefinitionByName(u'EventLogs')
    self.assertIsNotNone(artifact_definition)

    # Try to register something already registered
    with self.assertRaises(KeyError):
      artifact_registry.RegisterDefinition(artifact_definition)

    # Deregister
    artifact_registry.DeregisterDefinition(artifact_definition)

    # Check it is gone
    with self.assertRaises(KeyError):
      artifact_registry.DeregisterDefinition(artifact_definition)

    self.assertEqual(len(artifact_registry.GetDefinitions()), 6)

    test_artifact_definition = artifact_registry.GetDefinitionByName(
        u'SecurityEventLogEvtx')
    self.assertIsNotNone(test_artifact_definition)

    self.assertEqual(test_artifact_definition.name, u'SecurityEventLogEvtx')

    expected_description = (
        u'Windows Security Event log for Vista or later systems.')
    self.assertEqual(test_artifact_definition.description, expected_description)

    bad_args = io.BytesIO(
        b'name: SecurityEventLogEvtx\n'
        b'doc: Windows Security Event log for Vista or later systems.\n'
        b'sources:\n'
        b'- type: FILE\n'
        b'  attributes: {broken: [\'%%environ_systemroot%%\\System32\\'
        b'winevt\\Logs\\Security.evtx\']}\n'
        b'conditions: [os_major_version >= 6]\n'
        b'labels: [Logs]\n'
        b'supported_os: [Windows]\n'
        b'urls: [\'http://www.forensicswiki.org/wiki/\n'
        b'Windows_XML_Event_Log_(EVTX)\']\n')

    generator = artifact_reader.ReadFileObject(bad_args)
    with self.assertRaises(errors.FormatError):
      next(generator)


if __name__ == '__main__':
  unittest.main()
