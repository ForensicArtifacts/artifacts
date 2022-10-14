# -*- coding: utf-8 -*-
"""The artifact definition."""

from artifacts import errors
from artifacts import registry


class ArtifactDefinition(object):
  """Artifact definition interface.

  Attributes:
    aliases (list[str]): aliases that identify the artifact definition.
    description (str): description.
    name (str): name that uniquely identifiers the artifact definition.
    provides (list[str]): hints to what information the artifact definition
        provides.
    sources (list[str]): sources.
    supported_os (list[str]): supported operating systems.
    urls (list[str]): URLs with more information about the artifact definition.
  """

  def __init__(self, name, aliases=None, description=None):
    """Initializes an artifact definition.

    Args:
      name (str): name that uniquely identifiers the artifact definition.
      aliases (Optional[str]): aliases that identify the artifact definition.
      description (Optional[str]): description of the artifact definition.
    """
    super(ArtifactDefinition, self).__init__()
    self.aliases = aliases or []
    self.description = description
    self.name = name
    self.provides = []
    self.sources = []
    self.supported_os = []
    self.urls = []

  def AppendSource(self, type_indicator, attributes):
    """Appends a source.

    If you want to implement your own source type you should create a subclass
    in source_type.py and change the AppendSource method to handle the new
    subclass. This function raises FormatError if an unsupported source type
    indicator is encountered.

    Args:
      type_indicator (str): source type indicator.
      attributes (dict[str, object]): source attributes.

    Returns:
      SourceType: a source type.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
          or if required attributes are missing.
    """
    if not type_indicator:
      raise errors.FormatError('Missing type indicator.')

    try:
      source_object = registry.ArtifactDefinitionsRegistry.CreateSourceType(
          type_indicator, attributes)
    except (AttributeError, TypeError) as exception:
      raise errors.FormatError((
          f'Unable to create source type: {type_indicator:s} for artifact '
          f'definition: {self.name:s} with error: {exception!s}'))

    self.sources.append(source_object)
    return source_object

  def AsDict(self):
    """Represents an artifact as a dictionary.

    Returns:
      dict[str, object]: artifact attributes.
    """
    sources = []
    for source in self.sources:
      source_definition = {
          'type': source.type_indicator,
          'attributes': source.AsDict()
      }
      if source.supported_os:
        source_definition['supported_os'] = source.supported_os
      sources.append(source_definition)

    artifact_definition = {
        'name': self.name,
        'doc': self.description,
        'sources': sources,
    }
    if self.aliases:
      artifact_definition['aliases'] = self.aliases
    if self.supported_os:
      artifact_definition['supported_os'] = self.supported_os
    if self.provides:
      artifact_definition['provides'] = self.provides
    if self.urls:
      artifact_definition['urls'] = self.urls
    return artifact_definition
