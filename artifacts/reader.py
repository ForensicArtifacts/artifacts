# -*- coding: utf-8 -*-
"""The artifact reader objects."""

import abc
import glob
import io
import os
import json
import yaml

from artifacts import artifact
from artifacts import definitions
from artifacts import errors


class BaseArtifactsReader(object):
  """Artifacts reader interface.

  Attributes:
    supported_os (set[str]): supported operating systems.
  """

  # Note that redundant-returns-doc and redundant-yields-doc are broken for
  # pylint 1.7.x for abstract methods.
  # pylint: disable=redundant-returns-doc,redundant-yields-doc

  def __init__(self):
    """Initializes an artifacts reader."""
    super(BaseArtifactsReader, self).__init__()
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

  # Note that redundant-yields-doc is broken for pylint 1.7.x for
  # abstract methods.
  # pylint: disable=redundant-yields-doc

  def __init__(self):
    """Initializes an artifacts reader."""
    super(ArtifactsReader, self).__init__()
    self.supported_os = set(definitions.SUPPORTED_OS)

  # Pylint fails on detecting the type of definition_object based on
  # the docstring.
  # pylint: disable=missing-type-doc
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
      supported_os_type = type(supported_os)
      raise errors.FormatError(
          f'Invalid supported_os type: {supported_os_type!s}')

    undefined_supported_os = set(supported_os).difference(self.supported_os)
    if undefined_supported_os:
      undefined_supported_os = ', '.join(undefined_supported_os)
      raise errors.FormatError((
          f'Artifact definition: {name:s} undefined supported operating '
          f'system: {undefined_supported_os:s}.'))

    definition_object.supported_os = supported_os

  def _ReadSources(self, artifact_definition_values, artifact_definition, name):
    """Reads the artifact definition sources.

    Args:
      artifact_definition_values (dict[str, object]): artifact definition
          values.
      artifact_definition (ArtifactDefinition): an artifact definition.
      name (str): name of the artifact definition.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
          or if required attributes are missing.
    """
    sources = artifact_definition_values.get('sources')
    if not sources:
      raise errors.FormatError(
          f'Invalid artifact definition: {name:s} missing sources.')

    for source in sources:
      type_indicator = source.get('type', None)
      if not type_indicator:
        raise errors.FormatError(
            f'Invalid artifact definition: {name:s} source type.')

      attributes = source.get('attributes', None)

      try:
        source_type = artifact_definition.AppendSource(
            type_indicator, attributes)
      except errors.FormatError as exception:
        raise errors.FormatError(
            f'Invalid artifact definition: {name:s}, with error: {exception!s}')

      # TODO: deprecate these left overs from the collector definition.
      if source_type:
        if source.get('returned_types', None):
          raise errors.FormatError((
              f'Invalid artifact definition: {name:s} returned_types no longer '
              f'supported.'))

        self._ReadSupportedOS(source, source_type, name)
        if set(source_type.supported_os) - set(
            artifact_definition.supported_os):
          raise errors.FormatError((
              f'Invalid artifact definition: {name:s} missing '
              f'supported_os.'))

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
      raise errors.FormatError(f'Undefined keys: {different_keys:s}')

    name = artifact_definition_values.get('name', None)
    if not name:
      raise errors.FormatError('Invalid artifact definition missing name.')

    # The description is assumed to be mandatory.
    description = artifact_definition_values.get('doc', None)
    if not description:
      raise errors.FormatError(
          f'Invalid artifact definition: {name:s} missing description.')

    aliases = artifact_definition_values.get('aliases', None)

    artifact_definition = artifact.ArtifactDefinition(
        name, aliases=aliases, description=description)

    if artifact_definition_values.get('collectors', []):
      raise errors.FormatError(
          f'Invalid artifact definition: {name:s} still uses collectors.')

    urls = artifact_definition_values.get('urls', [])
    if not isinstance(urls, list):
      raise errors.FormatError(
          f'Invalid artifact definition: {name:s} urls is not a list.')

    artifact_definition.provides = artifact_definition_values.get(
        'provides', [])
    self._ReadSupportedOS(artifact_definition_values, artifact_definition, name)
    artifact_definition.urls = urls
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
      glob_spec = os.path.join(path, f'*.{extension:s}')
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
    with io.open(filename, 'r', encoding='utf-8') as file_object:
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
          error_location = f'After: {last_artifact_definition.name:s}'

        raise errors.FormatError(f'{error_location:s} {exception!s}')

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
          error_location = f'After: {last_artifact_definition.name:s}'

        raise errors.FormatError(f'{error_location:s} {exception!s}')

      yield artifact_definition
      last_artifact_definition = artifact_definition
