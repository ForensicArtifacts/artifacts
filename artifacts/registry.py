# -*- coding: utf-8 -*-
"""The artifact definitions registry."""

from artifacts import definitions


class ArtifactDefinitionsRegistry(object):
  """Class that implements an artifact definitions registry."""

  def __init__(self):
    """Initializes the artifact definitions registry object."""
    super(ArtifactDefinitionsRegistry, self).__init__()
    self._artifact_definitions = {}
    self._artifact_name_references = set()
    self._defined_artifact_names = set()

  def DeregisterDefinition(self, artifact_definition):
    """Deregisters an artifact definition.

    The artifact definitions are identified based on their lower case name.

    Args:
      artifact_definition: the artifact definitions (instance of
                           ArtifactDefinition).

    Raises:
      KeyError: if an artifact definition is not set for the corresponding name.
    """
    artifact_definition_name = artifact_definition.name.lower()
    if artifact_definition_name not in self._artifact_definitions:
      raise KeyError(u'Artifact definition not set for name: {0}.'.format(
          artifact_definition.name))

    del self._artifact_definitions[artifact_definition_name]

  def GetDefinitionByName(self, name):
    """Retrieves a specific artifact definition by name.

    Args:
      name: the name of the artifact definition.

    Returns:
      The artifact definition (instance of ArtifactDefinition) or None
      if not available.
    """
    if name:
      return self._artifact_definitions.get(name.lower(), None)

  def GetDefinitions(self):
    """Retrieves the artifact definitions.

    Returns:
      An array of ArtifactDefinition objects.
    """
    return self._artifact_definitions.values()

  def GetUndefinedArtifacts(self):
    """Retrieves the names of undefined artifacts used by artifact groups.

    Returns:
      A set of the undefined artifacts names.
    """
    return self._artifact_name_references - self._defined_artifact_names

  def RegisterDefinition(self, artifact_definition):
    """Registers an artifact definition.

    The artifact definitions are identified based on their lower case name.

    Args:
      artifact_definition: the artifact definitions (instance of
                           ArtifactDefinition).

    Raises:
      KeyError: if artifact definition is already set for the corresponding
                name.
    """
    artifact_definition_name = artifact_definition.name.lower()
    if artifact_definition_name in self._artifact_definitions:
      raise KeyError(u'Artifact definition already set for name: {0}.'.format(
          artifact_definition.name))

    self._artifact_definitions[artifact_definition_name] = artifact_definition
    self._defined_artifact_names.add(artifact_definition.name)

    for source in artifact_definition.sources:
      if source.type_indicator == definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
        self._artifact_name_references.update(source.names)

  def ReadFromDirectory(self, artifact_reader, path, extension=u'yaml'):
    """Reads artifact definitions into the registry from files in a directory.

    This function does not recurse sub directories.

    Args:
      artifacts_reader: an artifacts reader object (instance of
                        ArtifactsReader).
      path: the path of the directory to read from.
      extension: optional extension of the filenames to read.
                 The default is 'yaml'.

    Raises:
      KeyError: if a duplicate artifact definition is encountered.
    """
    for artifact_definition in artifact_reader.ReadDirectory(
        path, extension=extension):
      self.RegisterDefinition(artifact_definition)

  def ReadFromFile(self, artifact_reader, filename):
    """Reads artifact definitions into the registry from a file.

    Args:
      artifacts_reader: an artifacts reader object (instance of
                        ArtifactsReader).
      filename: the name of the file to read from.
    """
    for artifact_definition in artifact_reader.ReadFile(filename):
      self.RegisterDefinition(artifact_definition)

  def ReadFileObject(self, artifact_reader, file_object):
    """Reads artifact definitions into the registry from a file-like object.

    Args:
      artifacts_reader: an artifacts reader object (instance of
                        ArtifactsReader).
      file_object: the file-like object to read from.
    """
    for artifact_definition in artifact_reader.ReadFileObject(file_object):
      self.RegisterDefinition(artifact_definition)
