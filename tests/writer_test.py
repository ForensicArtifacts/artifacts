# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import os
import unittest
import json
import tempfile

from artifacts import reader
from artifacts import writer


class YamlArtifactsWriterTest(unittest.TestCase):
  """Class to test the YAML artifacts writer"""

  def testYamlWriter(self):
    """Tests the YamlArtifactsWriter FormatArtifacts method for loss during conversion."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.YamlArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    with tempfile.NamedTemporaryFile() as artifact_file:
      artifact_writer.WriteArtifactsFile(artifact_definitions,
                                         artifact_file.name)
      converted_artifact_definitions = list(artifact_reader.ReadFile(
          artifact_file.name))

    self.assertListEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])


class JsonArtifactsWriterTest(unittest.TestCase):
  """Class to test the JSON artifacts writer"""

  def testJsonWriter(self):
    """Tests the JsonArtifactsWriter FormatArtifacts method for loss during conversion."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.JsonArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    artifacts_json = artifact_writer.FormatArtifacts(artifact_definitions)

    converted_artifact_definitions = [
        artifact_reader.ReadArtifactDefinitionValues(artifact_definition)
        for artifact_definition in json.loads(artifacts_json)
    ]

    self.assertListEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])


if __name__ == '__main__':
  unittest.main()
