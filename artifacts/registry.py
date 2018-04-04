# -*- coding: utf-8 -*-
"""The artifact definitions registry."""

from __future__ import unicode_literals

from artifacts import definitions
from artifacts import errors
from artifacts import source_type


class ArtifactDefinitionsRegistry(object):
  """Artifact definitions registry."""

  _source_type_classes = {
      definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
          source_type.ArtifactGroupSourceType,
      definitions.TYPE_INDICATOR_COMMAND: source_type.CommandSourceType,
      definitions.TYPE_INDICATOR_DIRECTORY: source_type.DirectorySourceType,
      definitions.TYPE_INDICATOR_FILE: source_type.FileSourceType,
      definitions.TYPE_INDICATOR_PATH: source_type.PathSourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
          source_type.WindowsRegistryKeySourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
          source_type.WindowsRegistryValueSourceType,
      definitions.TYPE_INDICATOR_WMI_QUERY: source_type.WMIQuerySourceType,
  }

  def __init__(self):
    """Initializes an artifact definitions registry."""
    super(ArtifactDefinitionsRegistry, self).__init__()
    self._artifact_definitions = {}
    self._artifact_name_references = set()
    self._defined_artifact_names = set()

  @classmethod
  def CreateSourceType(cls, type_indicator, attributes):
    """Creates a source type object.

    Args:
      type_indicator (str): source type indicator.
      attributes (dict[str, object]): source attributes.

    Returns:
      SourceType: a source type.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
          or if required attributes are missing.
    """
    if type_indicator not in cls._source_type_classes:
      raise errors.FormatError(
          'Unsupported type indicator: {0:s}.'.format(type_indicator))

    return cls._source_type_classes[type_indicator](**attributes)

  def DeregisterDefinition(self, artifact_definition):
    """Deregisters an artifact definition.

    Artifact definitions are identified based on their lower case name.

    Args:
      artifact_definition (ArtifactDefinition): an artifact definition.

    Raises:
      KeyError: if an artifact definition is not set for the corresponding name.
    """
    artifact_definition_name = artifact_definition.name.lower()
    if artifact_definition_name not in self._artifact_definitions:
      raise KeyError(
          'Artifact definition not set for name: {0:s}.'.format(
              artifact_definition.name))

    del self._artifact_definitions[artifact_definition_name]

  @classmethod
  def DeregisterSourceType(cls, source_type_class):
    """Deregisters a source type.

    Source types are identified based on their type indicator.

    Args:
      source_type_class (type): source type.

    Raises:
      KeyError: if a source type is not set for the corresponding type
          indicator.
    """
    if source_type_class.TYPE_INDICATOR not in cls._source_type_classes:
      raise KeyError(
          'Source type not set for type: {0:s}.'.format(
              source_type_class.TYPE_INDICATOR))

    del cls._source_type_classes[source_type_class.TYPE_INDICATOR]

  def GetDefinitionByName(self, name):
    """Retrieves a specific artifact definition by name.

    Args:
      name (str): name of the artifact definition.

    Returns:
      ArtifactDefinition: an artifact definition or None if not available.
    """
    if name:
      return self._artifact_definitions.get(name.lower(), None)

  def GetDefinitions(self):
    """Retrieves the artifact definitions.

    Returns:
      list[ArtifactDefinition]: artifact definitions.
    """
    return self._artifact_definitions.values()

  def GetUndefinedArtifacts(self):
    """Retrieves the names of undefined artifacts used by artifact groups.

    Returns:
      set[str]: undefined artifacts names.
    """
    return self._artifact_name_references - self._defined_artifact_names

  def RegisterDefinition(self, artifact_definition):
    """Registers an artifact definition.

    Artifact definitions are identified based on their lower case name.

    Args:
      artifact_definition (ArtifactDefinition): an artifact definition.

    Raises:
      KeyError: if artifact definition is already set for the corresponding
          name.
    """
    artifact_definition_name = artifact_definition.name.lower()
    if artifact_definition_name in self._artifact_definitions:
      raise KeyError(
          'Artifact definition already set for name: {0:s}.'.format(
              artifact_definition.name))

    self._artifact_definitions[artifact_definition_name] = artifact_definition
    self._defined_artifact_names.add(artifact_definition.name)

    for source in artifact_definition.sources:
      if source.type_indicator == definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
        self._artifact_name_references.update(source.names)

  @classmethod
  def RegisterSourceType(cls, source_type_class):
    """Registers a source type.

    Source types are identified based on their type indicator.

    Args:
      source_type_class (type): source type.

    Raises:
      KeyError: if source types is already set for the corresponding
          type indicator.
    """
    if source_type_class.TYPE_INDICATOR in cls._source_type_classes:
      raise KeyError(
          'Source type already set for type: {0:s}.'.format(
              source_type_class.TYPE_INDICATOR))

    cls._source_type_classes[source_type_class.TYPE_INDICATOR] = (
        source_type_class)

  @classmethod
  def RegisterSourceTypes(cls, source_type_classes):
    """Registers source types.

    Source types are identified based on their type indicator.

    Args:
      source_type_classes (list[type]): source types.
    """
    for source_type_class in source_type_classes:
      cls.RegisterSourceType(source_type_class)

  def ReadFromDirectory(self, artifact_reader, path, extension='yaml'):
    """Reads artifact definitions into the registry from files in a directory.

    This function does not recurse sub directories.

    Args:
      artifacts_reader (ArtifactsReader): an artifacts reader.
      path (str): path of the directory to read from.
      extension (Optional[str]): extension of the filenames to read.

    Raises:
      KeyError: if a duplicate artifact definition is encountered.
    """
    for artifact_definition in artifact_reader.ReadDirectory(
        path, extension=extension):
      self.RegisterDefinition(artifact_definition)

  def ReadFromFile(self, artifact_reader, filename):
    """Reads artifact definitions into the registry from a file.

    Args:
      artifacts_reader (ArtifactsReader): an artifacts reader.
      filename (str): name of the file to read from.
    """
    for artifact_definition in artifact_reader.ReadFile(filename):
      self.RegisterDefinition(artifact_definition)

  def ReadFileObject(self, artifact_reader, file_object):
    """Reads artifact definitions into the registry from a file-like object.

    Args:
      artifacts_reader (ArtifactsReader): an artifacts reader.
      file_object (file): file-like object to read from.
    """
    for artifact_definition in artifact_reader.ReadFileObject(file_object):
      self.RegisterDefinition(artifact_definition)
