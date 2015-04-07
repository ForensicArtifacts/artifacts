# -*- coding: utf-8 -*-
"""Tests for the artifact definitions registry."""

import os
import unittest

from artifacts import reader
from artifacts import registry


class ArtifactDefinitionsRegistryTest(unittest.TestCase):
  """Tests for the artifact definitions registry."""

  def testArtifactDefinitionsRegistry(self):
    """Tests the ArtifactDefinitionsRegistry functions."""
    artifact_registry = registry.ArtifactDefinitionsRegistry()

    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definition = None
    with open(test_file, 'rb') as file_object:
      for artifact_definition in artifact_reader.Read(file_object):
        artifact_registry.RegisterDefinition(artifact_definition)

    # Make sure the test file is not empty.
    self.assertNotEquals(artifact_definition, None)

    with self.assertRaises(KeyError):
      artifact_registry.RegisterDefinition(artifact_definition)

    artifact_definitions = []
    for artifact_definition in artifact_registry.GetDefinitions():
      artifact_definitions.append(artifact_definition)

    artifact_registry.DeregisterDefinition(artifact_definition)

    with self.assertRaises(KeyError):
      artifact_registry.DeregisterDefinition(artifact_definition)

    artifact_definitions = []
    for artifact_definition in artifact_registry.GetDefinitions():
      artifact_definitions.append(artifact_definition)

    self.assertEqual(len(artifact_definitions), 6)

    test_artifact_definition = artifact_registry.GetDefinitionByName(
        'SecurityEventLogEvtx')
    self.assertNotEquals(test_artifact_definition, None)

    self.assertEquals(test_artifact_definition.name, u'SecurityEventLogEvtx')

    expected_description = (
        u'Windows Security Event log for Vista or later systems.')
    self.assertEquals(
        test_artifact_definition.description, expected_description)

    bad_args = """
name: SecurityEventLogEvtx
doc: Windows Security Event log for Vista or later systems.
collectors:
- collector_type: FILE
  args: {broken: ['%%environ_systemroot%%\System32\winevt\Logs\Security.evtx']}
conditions: [os_major_version >= 6]
labels: [Logs]
supported_os: [Windows]
urls: ['http://www.forensicswiki.org/wiki/Windows_XML_Event_Log_(EVTX)']
"""
    with self.assertRaises(TypeError):
      bad_artifact = artifact_reader.Read(bad_args).next()


if __name__ == '__main__':
  unittest.main()
