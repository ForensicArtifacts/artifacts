# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import os
import unittest
import yaml
import json

from artifacts import errors
from artifacts import reader
from artifacts import writer


class ArtifactAsDictTest(unittest.TestCase):
  """Class to test the artifacts AsDict conversion"""

  def testAsDict(self):
    """Tests the ArtifactDefinition AsDict method."""
    artifact_reader = reader.YamlArtifactsReader()
    test_file = os.path.join('test_data', 'definitions.yaml')

    with open(test_file, 'r') as file_object:
      for artifact_definition in yaml.safe_load_all(file_object):
        artifact_object = artifact_reader._ReadArtifactDefinition(
            artifact_definition)
        self.assertEqual(artifact_definition, artifact_object.AsDict())

  def testDefinitionsAsDict(self):
    """Tests that all defined artifacts can convert to dictionary representation."""
    artifact_reader = reader.YamlArtifactsReader()

    artifact_definitions = list(artifact_reader.ReadDirectory('definitions'))

    last_artifact_definition = None
    for artifact in artifact_definitions:
      try:
        artifact_definition = artifact.AsDict()
      except errors.FormatError:
        error_location = u'At start'
        if last_artifact_definition:
          error_location = u'After: {0}'.format(last_artifact_definition.name)
        self.fail(u'{0} failed to convert to dict'.format(error_location))
      last_artifact_definition = artifact_definition


class YamlArtifactsWriterTest(unittest.TestCase):
  """Class to test the YAML artifacts writer"""

  def testYamlWriter(self):
    """Tests the YamlArtifactsWriter FormatArtifacts method."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.YamlArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    artifacts_yaml = artifact_writer.FormatArtifacts(artifact_definitions)

    file_object = io.StringIO(initial_value=artifacts_yaml)
    converted_artifact_definitions = list(artifact_reader.ReadFileObject(
        file_object))
    self.assertCountEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])


class JsonArtifactsWriterTest(unittest.TestCase):
  """Class to test the JSON artifacts writer"""

  def testJsonWriter(self):
    """Tests the JsonArtifactsWriter FormatArtifacts method."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.JsonArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')

    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    artifacts_json = artifact_writer.FormatArtifacts(artifact_definitions)

    converted_artifact_definitions = [
        artifact_reader._ReadArtifactDefinition(artifact_definition)
        for artifact_definition in json.loads(artifacts_json)
    ]
    self.assertCountEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])


if __name__ == '__main__':
  unittest.main()
