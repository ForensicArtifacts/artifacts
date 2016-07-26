# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import os
import unittest
import json

from artifacts import reader
from artifacts import writer
import artifacts.py2to3 as py2to3


class YamlArtifactsWriterTest(unittest.TestCase):
  """Class to test the YAML artifacts writer"""

  def testYamlWriter(self):
    """Tests the YamlArtifactsWriter FormatArtifacts method for loss during conversion."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.YamlArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    artifacts_yaml = artifact_writer.FormatArtifacts(artifact_definitions)
    if isinstance(artifacts_yaml, py2to3.BYTES_TYPE):
      artifacts_yaml = artifacts_yaml.decode('ascii')

    file_object = io.StringIO(initial_value=artifacts_yaml)
    converted_artifact_definitions = list(artifact_reader.ReadFileObject(
        file_object))

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
    if isinstance(artifacts_json, py2to3.BYTES_TYPE):
      artifacts_json = artifacts_json.decode('ascii')
    converted_artifact_definitions = [
        artifact_reader.ReadArtifactDefinitionValues(artifact_definition)
        for artifact_definition in json.loads(artifacts_json)
    ]

    self.assertListEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])


if __name__ == '__main__':
  unittest.main()
