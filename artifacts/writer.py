# -*- coding: utf-8 -*-
"""The artifact writer objects."""

from __future__ import unicode_literals

import abc
import json
import yaml


class BaseArtifactsWriter(object):
  """Artifacts writer interface."""

  @abc.abstractmethod
  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts (list[ArtifactDefinition]): artifact definitions.

    Returns:
      str: formatted string of artifact definition.
    """

  @abc.abstractmethod
  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts (list[ArtifactDefinition]): artifact definitions to be written.
      filename (str): name of the file to write artifacts to.
    """


class ArtifactWriter(BaseArtifactsWriter):
  """File artifacts writer."""

  @abc.abstractmethod
  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts (ArtifactDefinition|list[ArtifactDefinition]): artifact
          definitions.

    Returns:
      str: formatted string of artifact definition.
    """

  def WriteArtifactsFile(self, artifacts, filename):
    """Writes artifact definitions to a file.

    Args:
      artifacts (list[ArtifactDefinition]): artifact definitions to be written.
      filename (str): name of the file to write artifacts to.
    """
    with open(filename, 'w') as file_object:
      file_object.write(self.FormatArtifacts(artifacts))


class JsonArtifactsWriter(ArtifactWriter):
  """JSON artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts (list[ArtifactDefinition]): artifact definitions.

    Returns:
      str: formatted string of artifact definition.
    """
    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    json_data = json.dumps(artifact_definitions)
    return json_data


class YamlArtifactsWriter(ArtifactWriter):
  """YAML artifacts writer interface."""

  def FormatArtifacts(self, artifacts):
    """Formats artifacts to desired output format.

    Args:
      artifacts (list[ArtifactDefinition]): artifact definitions.

    Returns:
      str: formatted string of artifact definition.
    """
    # TODO: improve output formatting of yaml
    artifact_definitions = [artifact.AsDict() for artifact in artifacts]
    yaml_data = yaml.safe_dump_all(artifact_definitions)
    return yaml_data
