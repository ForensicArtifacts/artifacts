# -*- coding: utf-8 -*-
"""The artifact writer objects."""

import abc
import json
import yaml


class BaseArtifactsWriter(object):
  """Class that implements the artifacts writer interface."""

  @abc.abstractmethod
  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts: a list of ArtifactDefinition objects to be written.

      filename: the filename to write artifacts to.
    """

  @abc.abstractmethod
  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts: an ArtifactDefinition instance or list of ArtifactDefinitions.

    Returns:
      formatted string of artifact definition.
    """


class ArtifactWriter(BaseArtifactsWriter):
  """Class that implements the artifacts writer interface."""

  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts: a list of ArtifactDefinition objects to be written.

      filename: the filename to write artifacts to.
    """
    with open(filename, 'w') as file_object:
      file_object.write(self.FormatArtifacts(artifacts))


class JsonArtifactsWriter(ArtifactWriter):
  """Class that implements the JSON artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts: a list of ArtifactDefinitions.

    Returns:
      formatted string of artifact definition.
    """
    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    json_data = json.dumps(artifact_definitions)
    return json_data


class YamlArtifactsWriter(ArtifactWriter):
  """Class that implements the YAML artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts: a list of ArtifactDefinitions.

    Returns:
      formatted string of artifact definition.
    """
    # TODO: improve output formatting of yaml
    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    yaml_data = yaml.safe_dump_all(artifact_definitions)
    return yaml_data
