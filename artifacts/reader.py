# -*- coding: utf-8 -*-
"""The artifact reader objects."""

import abc
import glob
import os
import json
import yaml

from artifacts import artifact
from artifacts import definitions
from artifacts import errors


class BaseArtifactsReader(object):
  """Class that implements the artifacts reader interface.

  Attributes:
    labels: set of strings of defined labels.
    supported_os: set of strings of supported operating systems.
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
      artifact_definition_values: dictionary containing the artifact definition
                                  values.

    Returns:
      An artifact definition (instance of ArtifactDefinition).

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
  """Class that implements the artifacts reader interface.

  Attributes:
    labels: set of strings of defined labels.
    supported_os: set of strings of supported operating systems.
  """

  def __init__(self):
    """Initializes an artifacts reader."""
    super(ArtifactsReader, self).__init__()
    self.labels = set(definitions.LABELS)
    self.supported_os = set(definitions.SUPPORTED_OS)

  def ReadArtifactDefinitionValues(self, artifact_definition_values):
    """Reads an artifact definition from a dictionary.

    Args:
      artifact_definition_values: dictionary containing the artifact definition
                                  values.

    Returns:
      An artifact definition (instance of ArtifactDefinition).

    Raises:
      FormatError: if the format of the artifact definition is not set
                   or incorrect.
    """
    if not artifact_definition_values:
      raise errors.FormatError(u'Missing artifact definition values.')

    different_keys = (
        set(artifact_definition_values) - definitions.TOP_LEVEL_KEYS)
    if different_keys:
      raise errors.FormatError(u'Undefined keys: {0}'.format(different_keys))

    name = artifact_definition_values.get(u'name', None)
    if not name:
      raise errors.FormatError(u'Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = artifact_definition_values.get(u'doc', None)
    if not description:
      raise errors.FormatError(
          u'Invalid artifact definition: {0} missing description.'.format(name))

    artifact_definition = artifact.ArtifactDefinition(
        name, description=description)

    if artifact_definition_values.get(u'collectors', []):
      raise errors.FormatError(
          u'Invalid artifact definition: {0} still uses collectors.'.format(
              name))

    # TODO: check conditions.
    artifact_definition.conditions = artifact_definition_values.get(
        u'conditions', [])
    artifact_definition.provides = artifact_definition_values.get(
        u'provides', [])
    self._ReadLabels(artifact_definition_values, artifact_definition, name)
    self._ReadSupportedOS(artifact_definition_values, artifact_definition, name)
    artifact_definition.urls = artifact_definition_values.get(u'urls', [])
    self._ReadSources(artifact_definition_values, artifact_definition, name)

    return artifact_definition

  def _ReadLabels(self, artifact_definition_values, artifact_definition, name):
    """Reads the optional artifact definition labels.

    Args:
      artifact_definition_values: dictionary containing the artifact definition
                                  values.
      artifact_definition: the artifact definition (instance of
                           ArtifactDefinition).

    Raises:
      FormatError: if there are undefined labels.
    """
    labels = artifact_definition_values.get(u'labels', [])

    undefined_labels = set(labels).difference(self.labels)
    if undefined_labels:
      raise errors.FormatError(
          u'Artifact definition: {0} found undefined labels: {1}.'.format(
              name, u', '.join(undefined_labels)))

    artifact_definition.labels = labels

  def _ReadSupportedOS(self, definition_values, definition_object, name):
    """Reads the optional artifact or source type supported OS.

    Args:
      definition_values: a dictionary containing the artifact defintion or
                         source type values.
      definition_object: the definition object (instance of ArtifactDefinition
                         or SourceType).
      name: string containing the name of the artifact definition.

    Raises:
      FormatError: if there are undefined supported operating systems.
    """
    supported_os = definition_values.get(u'supported_os', [])
    if not isinstance(supported_os, list):
      raise errors.FormatError(
          u'Invalid supported_os type: {0}'.format(type(supported_os)))

    undefined_supported_os = set(supported_os).difference(self.supported_os)
    if undefined_supported_os:
      error_string = (
          u'Artifact definition: {0} undefined supported operating system: '
          u'{1}.').format(name, u', '.join(undefined_supported_os))
      raise errors.FormatError(error_string)

    definition_object.supported_os = supported_os

  def _ReadSources(self, artifact_definition_values, artifact_definition, name):
    """Reads the artifact definition sources.

    Args:
      artifact_definition_values: dictionary containing the artifact definition
                                  values.
      artifact_definition: the artifact definition (instance of
                           ArtifactDefinition).09

    Raises:
      FormatError: if the type indicator is not set or unsupported,
                   or if required attributes are missing.
    """
    sources = artifact_definition_values.get(u'sources')
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
        source_type = artifact_definition.AppendSource(
            type_indicator, attributes)
      except errors.FormatError as exception:
        raise errors.FormatError(
            u'Invalid artifact definition: {0}. {1}'.format(name, exception))

      # TODO: deprecate these left overs from the collector definition.
      if source_type:
        source_type.conditions = source.get(u'conditions', [])
        source_type.returned_types = source.get(u'returned_types', [])
        self._ReadSupportedOS(source, source_type, name)
        if set(source_type.supported_os) - set(
            artifact_definition.supported_os):
          raise errors.FormatError(
              (u'Invalid artifact definition: {0} missing '
               u'supported_os.').format(name))

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
    with open(filename, 'r') as file_object:
      for artifact_definition in self.ReadFileObject(file_object):
        yield artifact_definition

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
        artifact_definition = self.ReadArtifactDefinitionValues(yaml_definition)
      except errors.FormatError as exception:
        error_location = u'At start'
        if last_artifact_definition:
          error_location = u'After: {0}'.format(last_artifact_definition.name)

        raise errors.FormatError(u'{0} {1}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition


class JsonArtifactsReader(ArtifactsReader):
  """Class that implements the JSON artifacts reader."""

  def ReadFileObject(self, file_object):
    """Reads artifact definitions from a file-like object.

    Args:
      file_object: the file-like object to read from.

    Yields:
      Artifact definitions (instances of ArtifactDefinition).

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
        error_location = u'At start'
        if last_artifact_definition:
          error_location = u'After: {0}'.format(last_artifact_definition.name)

        raise errors.FormatError(u'{0} {1}'.format(error_location, exception))

      yield artifact_definition
      last_artifact_definition = artifact_definition
