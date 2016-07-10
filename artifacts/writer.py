# -*- coding: utf-8 -*-
"""The artifact writer objects."""

import abc
import json
import yaml
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
    """Formats artifact desired output format

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

    artifact_definitions = [artifact.CopyToDict() for artifact in artifacts]

    return json.dumps(artifact_definitions)


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

    artifact_definitions = [artifact.CopyToDict() for artifact in artifacts]
    yaml_data = yaml.dump_all(artifact_definitions)

    return yaml_data
