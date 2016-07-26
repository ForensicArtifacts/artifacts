# -*- coding: utf-8 -*-
"""The artifact reader objects."""

import abc
import glob
import os
import yaml

from artifacts import artifact
from artifacts import definitions
from artifacts import errors
from artifacts import source_type


class BaseArtifactsReader(object):
  """Class that implements the artifacts reader interface."""

  LABELS = None
  SUPPORTED_OS = None
  TYPE_INDICATORS = None

  @property
  def supported_os(self):
    """The supported supported_os values.

    Raises:
      NotImplementedError: if the SUPPORTED_OS list is not defined.
    """
    if not self.SUPPORTED_OS:
      raise NotImplementedError(u'Invalid supported SUPPORTED_OS list.')
    return self.SUPPORTED_OS

  @property
  def labels(self):
    """The supported label values.

    Raises:
      NotImplementedError: if the LABELS list is not defined.
    """
    if not self.LABELS:
      raise NotImplementedError(u'Invalid supported LABELS list.')
    return self.LABELS

  @property
  def type_indicators(self):
    """The supported source type values.

    Raises:
      NotImplementedError: if the TYPE_INDICATORS list is not defined.
    """
    if not self.TYPE_INDICATORS:
      raise NotImplementedError(u'Invalid supported TYPE_INDICATORS list.')
    return self.TYPE_INDICATORS

  @abc.abstractmethod
  def ReadArtifactDefinition(self, artifact_definition):
    """Reads an artifact definition.

    Args:
      artifact_definition: the artifact definition as a dict.

    Returns:
      An artifact object (instance of ArtifactDefinition).

    Raises:
      FormatError: if the format of the artifact definition is not set
                   or incorrect.
    """

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


class ArtifactsReader(BaseArtifactsReader):

  LABELS = definitions.LABELS
  SUPPORTED_OS = definitions.SUPPORTED_OS
  TYPE_INDICATORS = source_type.SourceTypeFactory.GetSourceTypeIndicators()

  def ReadArtifactDefinition(self, artifact_definition):
    """Reads an artifact definition.

    Args:
      artifact_definition: the artifact definition as a dict.

    Returns:
      An artifact object (instance of ArtifactDefinition).

    Raises:
      FormatError: if the format of the artifact definition is not set
                   or incorrect.
    """
    if not artifact_definition:
      raise errors.FormatError(u'Missing definition.')

    different_keys = set(artifact_definition) - definitions.TOP_LEVEL_KEYS
    if different_keys:
      raise errors.FormatError(u'Undefined keys: {0}'.format(different_keys))

    name = artifact_definition.get(u'name', None)
    if not name:
      raise errors.FormatError(u'Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = artifact_definition.get(u'doc', None)
    if not description:
      raise errors.FormatError(
          u'Invalid artifact definition: {0} missing description.'.format(name))

    artifact_object = artifact.ArtifactDefinition(name, description=description)

    if artifact_definition.get(u'collectors', []):
      raise errors.FormatError(
          u'Invalid artifact definition: {0} still uses collectors.'.format(
              name))

    # TODO: check conditions.
    artifact_object.conditions = artifact_definition.get(u'conditions', [])
    artifact_object.provides = artifact_definition.get(u'provides', [])
    self._ReadLabels(artifact_definition, artifact_object)
    self._ReadSupportedOS(artifact_definition, artifact_object, name)
    artifact_object.urls = artifact_definition.get(u'urls', [])
    self._ReadSources(artifact_definition, artifact_object)

    return artifact_object

  def _ReadLabels(self, artifact_definition, artifact_object):
    """Reads the optional artifact definition labels.

    Args:
      artifact_definition: the artifact definition as a dict.
      artifact_object: the artifact definition object (instance of
                           ArtifactDefinition).
    Raises:
      FormatError: if there are undefined labels.
    """
    name = artifact_definition.get(u'name', None)
    labels = artifact_definition.get(u'labels', [])
    undefined_labels = [item for item in labels if item not in self.labels]

    if undefined_labels:
      raise errors.FormatError(
          u'Artifact definition: {0} label(s): {1} not defined.'.format(
              name, ', '.join(undefined_labels)))

    artifact_object.labels = artifact_definition.get(u'labels', [])

  def _ReadSupportedOS(self, definition, definition_object, name):
    """Reads the optional artifact or source type supported OS.
    Args:
      definition: the artifact or source definition as a dict.
      definition_object: the definition object (instance of ArtifactDefinition
                        or SourceType).
      name: string containing the name of the artifact definition.
    Raises:
      FormatError: if there are undefined supported operating systems.
    """
    supported_os = definition.get(u'supported_os', [])

    if not isinstance(supported_os, list):
      raise errors.FormatError(
          u'supported_os must be a list of strings, got: {0}'.format(
              supported_os))

    undefined_supported_os = [
        item for item in supported_os if item not in self.supported_os
    ]

    if undefined_supported_os:
      error_string = (
          u'Artifact definition: {0} supported operating system: {1} '
          u'not defined.').format(name, u', '.join(undefined_supported_os))
      raise errors.FormatError(error_string)

    definition_object.supported_os = supported_os

  def _ReadSources(self, artifact_definition, artifact_object):
    """Reads the artifact definition sources

    Args:
      artifact_definition: the artifact definition as a dict.
      artifact_object: the artifact definition object (instance of
                           ArtifactDefinition).

    Raises:
      FormatError: if the type indicator is not set or unsupported,
                   or if required attributes are missing.
    """

    name = artifact_definition.get(u'name', None)
    sources = artifact_definition.get(u'sources')

    if not sources:
      raise errors.FormatError(
          u'Invalid artifact definition: {0} missing sources.'.format(name))

    for source_definition in sources:
      type_indicator = source_definition.get(u'type', None)
      if not type_indicator:
        raise errors.FormatError(
            u'Invalid artifact definition: {0} source type.'.format(name))

      if type_indicator not in self.type_indicators:
        raise errors.FormatError(u'Unsupported type indicator: {0}.'.format(
            type_indicator))

      attributes = source_definition.get(u'attributes', None)

      try:
        source_object = artifact_object.AppendSource(type_indicator, attributes)
      except (TypeError, AttributeError) as e:
        raise errors.FormatError(
            "Invalid artifact definition for {0}: {1}".format(name, e))

      if source_object:
        # TODO: deprecate these left overs from the collector definition.
        source_object.conditions = source_definition.get(u'conditions', [])
        source_object.returned_types = source_definition.get(u'returned_types',
                                                             [])
        self._ReadSupportedOS(source_definition, source_object, name)

        for supported_os in source_object.supported_os:
          if supported_os not in artifact_object.supported_os:
            raise errors.FormatError(
                u'Invalid artifact definition: {0} missing supported_os.'.format(
                    name))

  def ReadDirectory(self, path, extension=u'yaml'):
    """Reads artifact definitions from files in a directory.

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

    for artifact_file in glob.glob(glob_spec):
      for artifact_definition in self.ReadFile(artifact_file):
        yield artifact_definition

  def ReadFile(self, filename):
    """Reads artifact definitions from a file.

    Args:
      filename: the name of the file to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).
    """
    with open(filename, 'rb') as file_object:
      for artifact_definition in self.ReadFileObject(file_object):
        yield artifact_definition


class YamlArtifactsReader(ArtifactsReader):
  """Class that implements the YAML artifacts reader."""

  def ReadFileObject(self, yaml_file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      yaml_file_object: the file-like object to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).

    Raises:
      FormatError: if the format of the YAML artifact definition is not set
                   or incorrect.
    """
    # TODO: add try, except?
    yaml_generator = yaml.safe_load_all(yaml_file_object)

    last_artifact_definition = None
    for yaml_definition in yaml_generator:
      try:
        artifact_definition = self.ReadArtifactDefinition(yaml_definition)
      except errors.FormatError as exception:
        error_location = u'At start'
        if last_artifact_definition:
          error_location = u'After: {0}'.format(last_artifact_definition.name)

        raise errors.FormatError(u'{0} {1}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition
