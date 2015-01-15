#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The artifact reader objects."""

import abc
import yaml

from artifacts import artifact
from artifacts import definitions
from artifacts import errors


class ArtifactsReader(object):
  """Class that implements the artifacts reader interface."""

  @abc.abstractmethod
  def Read(self, file_object):
    """Reads artifact definitions.

    Args:
      file_object: the file-like object to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """


class YamlArtifactsReader(ArtifactsReader):
  """Class that implements the YAML artifacts reader."""

  def _ReadArtifactDefinition(self, yaml_definition):
    """Reads an artifact definition.

    Args:
      yaml_definition: the YAML artifact definition.

    Returns:
      An artifact definition (instance of ArtifactDefinition).

    Raises:
      FormatError: if the format of the YAML artifact definition is not set
                   or incorrect.
    """
    if not yaml_definition:
      raise errors.FormatError(u'Missing YAML definition.')

    name = yaml_definition.get('name', None)
    if not name:
      raise errors.FormatError(u'Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = yaml_definition.get('doc', None)
    if not description:
      raise errors.FormatError(
          u'Invalid artifact definition: {0:s} missing description.'.format(
              name))

    artifact_definition = artifact.ArtifactDefinition(
        name, description=description)

    if yaml_definition.get('collectors', []):
      raise errors.FormatError(
          u'Invalid artifact definition: {0:s} still uses collectors.'.format(
              name))

    for source in yaml_definition.get('sources', []):
      type_indicator = source.get('type', None)
      if not type_indicator:
        raise errors.FormatError(
            u'Invalid artifact definition: {0:s} source type.'.format(name))

      attributes = source.get('attributes', None)
      source_type = artifact_definition.AppendSource(
          type_indicator, attributes)

      # TODO: deprecate these left overs from the collector definition.
      if source_type:
        source_type.conditions = source.get('conditions', [])
        source_type.returned_types = source.get('returned_types', [])
        self._ReadSupportedOS(yaml_definition, source_type, name)

    # TODO: check conditions.
    artifact_definition.conditions = yaml_definition.get('conditions', [])
    artifact_definition.provides = yaml_definition.get('provides', [])
    self._ReadLabels(yaml_definition, artifact_definition, name)
    self._ReadSupportedOS(yaml_definition, artifact_definition, name)
    artifact_definition.urls = yaml_definition.get('urls', [])

    return artifact_definition

  def _ReadLabels(self, yaml_definition, artifact_definition, name):
    """Reads the optional artifact definition labels.

    Args:
      yaml_definition: the YAML artifact definition.
      artifact_definition: the artifact definition object (instance of
                           ArtifactDefinition).

    Raises:
      FormatError: if there are undefined labels.
    """
    labels = yaml_definition.get('labels', [])
    undefined_labels = [
        item for item in labels if item not in definitions.LABELS]

    if undefined_labels:
      raise errors.FormatError(
          u'Artifact definition: {0:s} label(s): {1:s} not defined.'.format(
              name, ', '.join(undefined_labels)))

    artifact_definition.labels = yaml_definition.get('labels', [])

  def _ReadSupportedOS(self, yaml_definition, definition_object, name):
    """Reads the optional artifact or source type supported OS.

    Args:
      yaml_definition: the YAML artifact definition.
      defintion_object: the definition object (instance of ArtifactDefinition
                        or SourceType).
      name: string containing the name of the arifact defintion.

    Raises:
      FormatError: if there are undefined supported operating systems.
    """
    supported_os = yaml_definition.get('supported_os', [])

    if not isinstance(supported_os, list):
      raise errors.FormatError(
          u'supported_os must be a list of strings, got: {0:s}'.format(
              supported_os))

    undefined_supported_os = [
        item for item in supported_os if item not in definitions.SUPPORTED_OS]

    if undefined_supported_os:
      raise errors.FormatError((
          u'Artifact definition: {0:s} supported operating system: {1:s} '
          u'not defined.').format(name, ', '.join(undefined_supported_os)))

    definition_object.supported_os = supported_os

  def Read(self, file_object):
    """Reads artifact definitions.

    Args:
      file_object: the file-like object to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """
    # TODO: add try, except?
    yaml_generator = yaml.safe_load_all(file_object)

    for yaml_definition in yaml_generator:
      yield self._ReadArtifactDefinition(yaml_definition)

  # TODO: add a read from directory method.
