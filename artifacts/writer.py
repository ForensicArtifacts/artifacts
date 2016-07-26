# -*- coding: utf-8 -*-
"""The artifact writer objects."""

import abc
import json
import yaml

import artifacts.py2to3 as py2to3
from artifacts.artifact import ArtifactDefinition


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
    with open(filename, 'wb') as file_object:
      file_object.write(self.FormatArtifacts(artifacts))


class JsonArtifactsWriter(ArtifactWriter):
  """Class that implements the JSON artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts: an ArtifactDefinition instance or list of ArtifactDefinitions.

    Returns:
      formatted string of artifact definition.
    """
    if isinstance(artifacts, ArtifactDefinition):
      artifacts = [artifacts]

    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    json_data = json.dumps(artifact_definitions)
    if isinstance(json_data, py2to3.BYTES_TYPE):
      try:
        return json_data.decode('ascii')
      except UnicodeDecodeError:
        pass
    else:
      return json_data


class YamlArtifactsWriter(ArtifactWriter):
  """Class that implements the YAML artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts: an ArtifactDefinition instance or list of ArtifactDefinitions.

    Returns:
      formatted string of artifact definition.
    """
    # TODO: improve output formatting of yaml
    if isinstance(artifacts, ArtifactDefinition):
      artifacts = [artifacts]

    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    yaml_data = yaml.safe_dump_all(artifact_definitions)
    if isinstance(yaml_data, py2to3.BYTES_TYPE):
      try:
        return yaml_data.decode('ascii')
      except UnicodeDecodeError:
        pass
    else:
      return yaml_data
