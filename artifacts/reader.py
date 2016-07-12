# -*- coding: utf-8 -*-
"""The artifact reader objects."""

import abc
import glob
import os

from artifacts import artifact
from artifacts import definitions
from artifacts import errors

import yaml


class ArtifactsReader(object):
  """Class that implements the artifacts reader interface."""

  @abc.abstractmethod
  def ReadDirectory(self, path, extension=None):
    """Reads artifact definitions from a directory.

    This function does not recurse sub directories.

    Args:
      path: the path of the directory to read from.
      extension: optional extension of the filenames to read.
                 The default is None.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """

  @abc.abstractmethod
  def ReadFile(self, filename):
    """Reads artifact definitions from a file.

    Args:
      filename: the name of the file to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """

  @abc.abstractmethod
  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

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

    different_keys = set(yaml_definition) - definitions.TOP_LEVEL_KEYS
    if different_keys:
      raise errors.FormatError(u'Undefined keys: {0}'.format(different_keys))

    name = yaml_definition.get(u'name', None)
    if not name:
      raise errors.FormatError(u'Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = yaml_definition.get(u'doc', None)
    if not description:
      raise errors.FormatError(
          u'Invalid artifact definition: {0} missing description.'.format(name))

    artifact_definition = artifact.ArtifactDefinition(name,
                                                      description=description)

    if yaml_definition.get(u'collectors', []):
      raise errors.FormatError(
          u'Invalid artifact definition: {0} still uses collectors.'.format(
              name))

    sources = yaml_definition.get(u'sources')
    if not sources:
      raise errors.FormatError(
          u'Invalid artifact definition: {0} missing sources.'.format(name))

    for source in sources:
      type_indicator = source.get(u'type', None)
      if not type_indicator:
        raise errors.FormatError(
            u'Invalid artifact definition: {0} source type.'.format(name))

      attributes = source.get(u'attributes', None)
      try:
        source_type = artifact_definition.AppendSource(type_indicator,
                                                       attributes)
      except errors.FormatError as exception:
        raise errors.FormatError(
            u'Invalid artifact definition: {0}. {1}'.format(name, exception))

      # TODO: deprecate these left overs from the collector definition.
      if source_type:
        source_type.conditions = source.get(u'conditions', [])
        source_type.returned_types = source.get(u'returned_types', [])
        self._ReadSupportedOS(yaml_definition, source_type, name)

    # TODO: check conditions.
    artifact_definition.conditions = yaml_definition.get(u'conditions', [])
    artifact_definition.provides = yaml_definition.get(u'provides', [])
    self._ReadLabels(yaml_definition, artifact_definition, name)
    self._ReadSupportedOS(yaml_definition, artifact_definition, name)
    artifact_definition.urls = yaml_definition.get(u'urls', [])

    return artifact_definition

  def _ReadLabels(self, yaml_definition, artifact_definition, name):
    """Reads the optional artifact definition labels.

    Args:
      yaml_definition: the YAML artifact definition.
      artifact_definition: the artifact definition object (instance of
                           ArtifactDefinition).
      name: string containing the name of the artifact definition.

    Raises:
      FormatError: if there are undefined labels.
    """
    labels = yaml_definition.get(u'labels', [])
    undefined_labels = [
        item for item in labels if item not in definitions.LABELS
    ]

    if undefined_labels:
      raise errors.FormatError(
          u'Artifact definition: {0} label(s): {1} not defined.'.format(
              name, ', '.join(undefined_labels)))

    artifact_definition.labels = yaml_definition.get(u'labels', [])

  def _ReadSupportedOS(self, yaml_definition, definition_object, name):
    """Reads the optional artifact or source type supported OS.

    Args:
      yaml_definition: the YAML artifact definition.
      definition_object: the definition object (instance of ArtifactDefinition
                        or SourceType).
      name: string containing the name of the artifact definition.

    Raises:
      FormatError: if there are undefined supported operating systems.
    """
    supported_os = yaml_definition.get(u'supported_os', [])

    if not isinstance(supported_os, list):
      raise errors.FormatError(
          u'supported_os must be a list of strings, got: {0}'.format(
              supported_os))

    undefined_supported_os = [
        item for item in supported_os if item not in definitions.SUPPORTED_OS
    ]

    if undefined_supported_os:
      error_string = (
          u'Artifact definition: {0} supported operating system: {1} '
          u'not defined.').format(name, u', '.join(undefined_supported_os))
      raise errors.FormatError(error_string)

    definition_object.supported_os = supported_os

  def ReadDirectory(self, path, extension=u'yaml'):
    """Reads artifact definitions from YAML files in a directory.

    This function does not recurse sub directories.

    Args:
      path: the path of the directory to read from.
      extension: optional extension of the filenames to read.
                 The default is 'yaml'.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """
    if extension:
      glob_spec = os.path.join(path, u'*.{0}'.format(extension))
    else:
      glob_spec = os.path.join(path, u'*')

    for yaml_file in glob.glob(glob_spec):
      for artifact_definition in self.ReadFile(yaml_file):
        yield artifact_definition

  def ReadFile(self, filename):
    """Reads artifact definitions from a YAML file.

    Args:
      filename: the name of the file to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """
    with open(filename, 'rb') as file_object:
      for artifact_definition in self.ReadFileObject(file_object):
        yield artifact_definition

  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object: the file-like object to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).

    Raises:
      FormatError: if the format of the YAML artifact definition is not set
                   or incorrect.
    """
    # TODO: add try, except?
    yaml_generator = yaml.safe_load_all(file_object)

    last_artifact_definition = None
    for yaml_definition in yaml_generator:
      try:
        artifact_definition = self._ReadArtifactDefinition(yaml_definition)
      except errors.FormatError as exception:
        error_location = u'At start'
        if last_artifact_definition:
          error_location = u'After: {0}'.format(last_artifact_definition.name)

        raise errors.FormatError(u'{0} {1}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition
