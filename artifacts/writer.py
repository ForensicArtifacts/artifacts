# -*- coding: utf-8 -*-
"""The artifact writer objects."""

import abc
import json
import yaml

class BaseArtifactsWriter(object):
  """Class that implements the artifacts reader interface."""

  @abc.abstractmethod
  def _ConvertArtifact(self, artifact):
    """Converts artifacts to dict from ArtifactDefinition objects

    Args:
      artifact: an instances of ArtifactDefinition

    Yields:
      dict representation of ArtifactDefinition instance
    """

  @abc.abstractmethod
  def WriteArtifacts(self, artifacts, filename):
    """Reads artifact definitions from a file.

    Args:
      artifacts: list of ArtifactDefinition objects to be written

      filename: filename to write artifacts to

    Yields:
      writes artifacts to file
    """

  @abc.abstractmethod
  def FormatArtifacts(self, artifacts):
    """Formats artifact desired output format

    Args:
      artifacts: an instance or list of ArtifactDefinition

    Yields:
      formatted string of artifact_definition
    """


class ArtifactWriter(BaseArtifactsWriter):

  def _ConvertArtifact(self, artifact):
    """Converts artifacts to dict from ArtifactDefinition objects

    Args:
      artifact: an instances of ArtifactDefinition

    Yields:
      dict representation of ArtifactDefinition instance
    """
    sources = []
    for source in artifact.sources:
      source_definition = {
        'type': source.type_indicator,
        'attributes': source.CopyToDict()
      }
      if source.supported_os:
        source_definition['supported_os'] = source.supported_os
      if source.conditions:
        source_definition['conditions'] = source.conditions
      if source.returned_types:
        source_definition['returned_types'] = source.returned_types
      sources.append(source_definition)

    artifact_definition = {
      'name': artifact.name,
      'doc': artifact.description,
      'sources': sources,
    }
    if artifact.labels:
      artifact_definition['labels'] = artifact.labels
    if artifact.supported_os:
      artifact_definition['supported_os'] = artifact.supported_os
    if artifact.provides:
      artifact_definition['provides'] = artifact.provides
    if artifact.conditions:
      artifact_definition['conditions'] = artifact.conditions
    if artifact.urls:
      artifact_definition['urls'] = artifact.urls
    return artifact_definition

  def WriteArtifacts(self, artifacts, filename):
    with open(filename, 'w') as file_object:
      file_object.write(self.FormatArtifacts(artifacts))


class JsonArtifactsWriter(ArtifactWriter):

  def FormatArtifacts(self, artifacts):
    """Converts artifacts to dict from ArtifactDefinition objects

    Args:
      artifacts: an instance or list of ArtifactDefinition

    Returns:
      formatted string of artifact_definition
    """

    if isinstance(artifacts, list):
      artifact_definitions = [self._ConvertArtifact(artifact) for artifact in artifacts]
    else:
      artifact_definitions = self._ConvertArtifact(artifacts)

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
    if isinstance(artifacts, list):
      artifact_definitions = [self._ConvertArtifact(artifact) for artifact in artifacts]
      yaml_data = yaml.dump_all(artifact_definitions)
    else:
      artifact_definitions = self._ConvertArtifact(artifacts)
      yaml_data = yaml.dump(artifact_definitions)
    return yaml_data
