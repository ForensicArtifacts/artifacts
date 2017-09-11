# -*- coding: utf-8 -*-
"""The artifact reader objects."""

from __future__ import unicode_literals

import abc
import glob
import os
import json
import yaml

from artifacts import artifact
from artifacts import definitions
from artifacts import errors


class BaseArtifactsReader(object):
  """Artifacts reader interface.

  Attributes:
    labels (set[str]): defined labels.
    supported_os (set[str]): supported operating systems.
  """

  def __init__(self):
    """Initializes an artifacts reader."""
    super(BaseArtifactsReader, self).__init__()
    self.labels = set()
    self.supported_os = set()

  @abc.abstractmethod
  def ReadArtifactDefinitionValues(self, artifact_definition_values):
    """Reads an artifact definition from a dictionary.

    Args:
      artifact_definition_values (dict[str, object]): artifact definition
          values.

    Returns:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the artifact definition is not set
          or incorrect.
    """

  @abc.abstractmethod
  def ReadDirectory(self, path, extension=None):
    """Reads artifact definitions from a directory.

    This function does not recurse sub directories.

    Args:
      path (str): path of the directory to read from.
      extension (Optional[str]): extension of the filenames to read.

    Yields:
      ArtifactDefinition: an artifact definition.
    """

  @abc.abstractmethod
  def ReadFile(self, filename):
    """Reads artifact definitions from a file.

    Args:
      filename (str): name of the file to read from.

    Yields:
      ArtifactDefinition: an artifact definition.
    """

  @abc.abstractmethod
  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object (file): file-like object to read from.

    Yields:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the artifact definition is not set
          or incorrect.
    """


class ArtifactsReader(BaseArtifactsReader):
  """Artifacts reader common functionality."""

  def __init__(self):
    """Initializes an artifacts reader."""
    super(ArtifactsReader, self).__init__()
    self.labels = set(definitions.LABELS)
    self.supported_os = set(definitions.SUPPORTED_OS)

  def _ReadLabels(self, artifact_definition_values, artifact_definition, name):
    """Reads the optional artifact definition labels.

    Args:
      artifact_definition_values (dict[str, object]): artifact definition
          values.
      artifact_definition (ArtifactDefinition): an artifact definition.

    Raises:
      FormatError: if there are undefined labels.
    """
    labels = artifact_definition_values.get('labels', [])

    undefined_labels = set(labels).difference(self.labels)
    if undefined_labels:
      raise errors.FormatError(
          'Artifact definition: {0:s} found undefined labels: {1:s}.'.format(
              name, ', '.join(undefined_labels)))

    artifact_definition.labels = labels

  def _ReadSupportedOS(self, definition_values, definition_object, name):
    """Reads the optional artifact or source type supported OS.

    Args:
      definition_values (dict[str, object]): artifact definition values.
      definition_object (ArtifactDefinition|SourceType): the definition object.
      name (str): name of the artifact definition.

    Raises:
      FormatError: if there are undefined supported operating systems.
    """
    supported_os = definition_values.get('supported_os', [])
    if not isinstance(supported_os, list):
      raise errors.FormatError(
          'Invalid supported_os type: {0!s}'.format(type(supported_os)))

    undefined_supported_os = set(supported_os).difference(self.supported_os)
    if undefined_supported_os:
      error_string = (
          'Artifact definition: {0:s} undefined supported operating system: '
          '{1:s}.').format(name, ', '.join(undefined_supported_os))
      raise errors.FormatError(error_string)

    definition_object.supported_os = supported_os

  def _ReadSources(self, artifact_definition_values, artifact_definition, name):
    """Reads the artifact definition sources.

    Args:
      artifact_definition_values (dict[str, object]): artifact definition
          values.
      artifact_definition (ArtifactDefinition): an artifact definition.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
          or if required attributes are missing.
    """
    sources = artifact_definition_values.get('sources')
    if not sources:
      raise errors.FormatError(
          'Invalid artifact definition: {0:s} missing sources.'.format(name))

    for source in sources:
      type_indicator = source.get('type', None)
      if not type_indicator:
        raise errors.FormatError(
            'Invalid artifact definition: {0:s} source type.'.format(name))

      attributes = source.get('attributes', None)

      try:
        source_type = artifact_definition.AppendSource(
            type_indicator, attributes)
      except errors.FormatError as exception:
        raise errors.FormatError(
            'Invalid artifact definition: {0:s}, with error: {1!s}'.format(
                name, exception))

      # TODO: deprecate these left overs from the collector definition.
      if source_type:
        source_type.conditions = source.get('conditions', [])
        source_type.returned_types = source.get('returned_types', [])
        self._ReadSupportedOS(source, source_type, name)
        if set(source_type.supported_os) - set(
            artifact_definition.supported_os):
          raise errors.FormatError(
              ('Invalid artifact definition: {0:s} missing '
               'supported_os.').format(name))

  def ReadArtifactDefinitionValues(self, artifact_definition_values):
    """Reads an artifact definition from a dictionary.

    Args:
      artifact_definition_values (dict[str, object]): artifact definition
          values.

    Returns:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the artifact definition is not set
          or incorrect.
    """
    if not artifact_definition_values:
      raise errors.FormatError('Missing artifact definition values.')

    different_keys = (
        set(artifact_definition_values) - definitions.TOP_LEVEL_KEYS)
    if different_keys:
      different_keys = ', '.join(different_keys)
      raise errors.FormatError('Undefined keys: {0:s}'.format(different_keys))

    name = artifact_definition_values.get('name', None)
    if not name:
      raise errors.FormatError('Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = artifact_definition_values.get('doc', None)
    if not description:
      raise errors.FormatError(
          'Invalid artifact definition: {0:s} missing description.'.format(
              name))

    artifact_definition = artifact.ArtifactDefinition(
        name, description=description)

    if artifact_definition_values.get('collectors', []):
      raise errors.FormatError(
          'Invalid artifact definition: {0:s} still uses collectors.'.format(
              name))

    # TODO: check conditions.
    artifact_definition.conditions = artifact_definition_values.get(
        'conditions', [])
    artifact_definition.provides = artifact_definition_values.get(
        'provides', [])
    self._ReadLabels(artifact_definition_values, artifact_definition, name)
    self._ReadSupportedOS(artifact_definition_values, artifact_definition, name)
    artifact_definition.urls = artifact_definition_values.get('urls', [])
    self._ReadSources(artifact_definition_values, artifact_definition, name)

    return artifact_definition

  def ReadDirectory(self, path, extension='yaml'):
    """Reads artifact definitions from a directory.

    This function does not recurse sub directories.

    Args:
      path (str): path of the directory to read from.
      extension (Optional[str]): extension of the filenames to read.

    Yields:
      ArtifactDefinition: an artifact definition.
    """
    if extension:
      glob_spec = os.path.join(path, '*.{0:s}'.format(extension))
    else:
      glob_spec = os.path.join(path, '*')

    for artifact_file in glob.glob(glob_spec):
      for artifact_definition in self.ReadFile(artifact_file):
        yield artifact_definition

  def ReadFile(self, filename):
    """Reads artifact definitions from a file.

    Args:
      filename (str): name of the file to read from.

    Yields:
      ArtifactDefinition: an artifact definition.
    """
    with open(filename, 'r') as file_object:
      for artifact_definition in self.ReadFileObject(file_object):
        yield artifact_definition

  @abc.abstractmethod
  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object (file): file-like object to read from.

    Yields:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the artifact definition is not set
          or incorrect.
    """


class JsonArtifactsReader(ArtifactsReader):
  """JSON artifacts reader."""

  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object (file): file-like object to read from.

    Yields:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the JSON artifact definition is not set
          or incorrect.
    """
    # TODO: add try, except?
    json_definitions = json.loads(file_object.read())

    last_artifact_definition = None
    for json_definition in json_definitions:
      try:
        artifact_definition = self.ReadArtifactDefinitionValues(json_definition)
      except errors.FormatError as exception:
        error_location = 'At start'
        if last_artifact_definition:
          error_location = 'After: {0:s}'.format(last_artifact_definition.name)

        raise errors.FormatError(
            '{0:s} {1!s}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition


class YamlArtifactsReader(ArtifactsReader):
  """YAML artifacts reader."""

  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object (file): file-like object to read from.

    Yields:
      ArtifactDefinition: an artifact definition.

    Raises:
      FormatError: if the format of the YAML artifact definition is not set
          or incorrect.
    """
    # TODO: add try, except?
    yaml_generator = yaml.safe_load_all(file_object)

    last_artifact_definition = None
    for yaml_definition in yaml_generator:
      try:
        artifact_definition = self.ReadArtifactDefinitionValues(yaml_definition)
      except errors.FormatError as exception:
        error_location = 'At start'
        if last_artifact_definition:
          error_location = 'After: {0:s}'.format(last_artifact_definition.name)

        raise errors.FormatError(
            '{0:s} {1!s}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition
