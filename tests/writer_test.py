# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

import io
import os
import unittest
import json
import tempfile

from artifacts import reader
from artifacts import writer


class ArtifactsWriterTest(unittest.TestCase):
  """Class to test the artifacts writer."""

  def checkArtifactConversion(self, artifact_reader, artifact_writer,
                              test_file):
    artifact_definitions = list(artifact_reader.ReadFile(test_file))
    with tempfile.NamedTemporaryFile() as artifact_file:
      artifact_writer.WriteArtifactsFile(artifact_definitions,
                                         artifact_file.name)
      converted_artifact_definitions = list(artifact_reader.ReadFile(
          artifact_file.name))

    self.assertListEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])

  def testYamlWriter(self):
    """Tests the YamlArtifactsWriter FormatArtifacts method for loss during conversion."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.YamlArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.yaml')
    self.checkArtifactConversion(artifact_reader, artifact_writer, test_file)

  def testJsonWriter(self):
    """Tests the JsonArtifactsWriter FormatArtifacts method for loss during conversion."""
    artifact_reader = reader.JsonArtifactsReader()
    artifact_writer = writer.JsonArtifactsWriter()
    test_file = os.path.join('test_data', 'definitions.json')
    self.checkArtifactConversion(artifact_reader, artifact_writer, test_file)


if __name__ == '__main__':
  unittest.main()
