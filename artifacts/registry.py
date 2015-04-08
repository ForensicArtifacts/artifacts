# -*- coding: utf-8 -*-
"""The artifact definitions registry."""


class ArtifactDefinitionsRegistry(object):
  """Class that implements the artifact definitions registry."""

  def __init__(self):
    """Initializes the artifact definitions registry object."""
    super(ArtifactDefinitionsRegistry, self).__init__()
    self._artifact_definitions = {}

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
      raise KeyError(
          u'Artifact definition not set for name: {0:s}.'.format(
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

    Yields:
      An artifact definitions (instances of ArtifactDefinition).
    """
    for artifact_definition in self._artifact_definitions.itervalues():
      yield artifact_definition

  def RegisterDefinition(self, artifact_definition):
    """Registers an artifact definition.

    The artifact definitiones are identified based on their lower case name.

    Args:
      artifact_definition: the artifact definitions (instance of
                           ArtifactDefinition).

    Raises:
      KeyError: if artifact definition is already set for the corresponding
                name.
    """
    artifact_definition_name = artifact_definition.name.lower()
    if artifact_definition_name in self._artifact_definitions:
      raise KeyError((
          u'Artifact definition already set for name: {0:s}.').format(
              artifact_definition.name))

    self._artifact_definitions[artifact_definition_name] = artifact_definition
