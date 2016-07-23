# -*- coding: utf-8 -*-
"""The artifact writer objects."""

import abc
import json
import yaml
import sys
from artifacts.artifact import ArtifactDefinition


class BaseArtifactsWriter(object):
  """Class that implements the artifacts reader interface."""

  @abc.abstractmethod
  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts: list of ArtifactDefinition objects to be written

      filename: filename to write artifacts to
    """

  @abc.abstractmethod
  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format

    Args:
      artifacts: an instance or list of ArtifactDefinition

    Returns:
      formatted string of artifact_definition
    """


class ArtifactWriter(BaseArtifactsWriter):

  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts: list of ArtifactDefinition objects to be written

      filename: filename to write artifacts to
    """
    with open(filename, 'wb') as file_object:
      file_object.write(self.FormatArtifacts(artifacts))


class JsonArtifactsWriter(ArtifactWriter):

  def FormatArtifacts(self, artifacts):
    """Converts artifacts to dict from ArtifactDefinition objects

    Args:
      artifacts: an instance or list of ArtifactDefinition

    Returns:
      formatted string of artifact_definition
    """
    if isinstance(artifacts, ArtifactDefinition):
      artifacts = [artifacts]

    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    json_data = json.dumps(artifact_definitions)
    if sys.version_info <= (3, 0):
      json_data = unicode(json_data)

    return json_data


class YamlArtifactsWriter(ArtifactWriter):

  def FormatArtifacts(self, artifacts):
    """Converts artifacts to dict from ArtifactDefinition objects

    Args:
      artifacts: a list of instances of ArtifactDefinition

    Returns:
      formatted string of artifact_definitions
    """
    # TODO: improve output formatting of yaml
    if isinstance(artifacts, ArtifactDefinition):
      artifacts = [artifacts]

    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    yaml_data = yaml.safe_dump_all(artifact_definitions)

    if sys.version_info <= (3, 0):
      yaml_data = unicode(yaml_data)

    return yaml_data
