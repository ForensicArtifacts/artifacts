# -*- coding: utf-8 -*-
"""The reader objects."""

from artifacts import definitions
from artifacts import errors
from artifacts import source_type


class ArtifactDefinition(object):
  """Class that implements the artifact reader interface."""

  def __init__(self, name, description=None):
    """Initializes the artifact definition object.

    Args:
      name: the name that uniquely identifiers the artifact definition.
      description: optional description of the artifact definition.
                   The default is None.
    """
    super(ArtifactDefinition, self).__init__()
    self.conditions = []
    self.description = description
    self.name = name
    self.labels = []
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
      type_indicator: the source type indicator.
      attributes: a dictionary containing the source attributes.

    Returns:
      The source type object (instance of SourceType) or None if the type
      indicator is not supported.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
                   or if required attributes are missing.
    """
    if not type_indicator:
      raise errors.FormatError(u'Missing type indicator.')

    if type_indicator == definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
      source_type_class = source_type.ArtifactGroupSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_COMMAND:
      source_type_class = source_type.CommandSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_DIRECTORY:
      source_type_class = source_type.DirectorySourceType

    elif type_indicator == definitions.TYPE_INDICATOR_FILE:
      source_type_class = source_type.FileSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_PATH:
      source_type_class = source_type.PathSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
      source_type_class = source_type.WindowsRegistryKeySourceType

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
      source_type_class = source_type.WindowsRegistryValueSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_WMI_QUERY:
      source_type_class = source_type.WMIQuerySourceType

    else:
      raise errors.FormatError(u'Unsupported type indicator: {0}.'.format(
          type_indicator))

    try:
      source_object = source_type_class(**attributes)
    except (TypeError, AttributeError) as e:
      raise errors.FormatError(
          u'Invalid artifact definition for {0}: {1}'.format(self.name, e))

    self.sources.append(source_object)
    return source_object

  def AsDict(self):
    """Converts artifact to dict from ArtifactDefinition

    Returns:
      dict representation of ArtifactDefinition instance
    """
    sources = []
    for source in self.sources:
      source_definition = {
          'type': source.type_indicator,
          'attributes': source.AsDict()
      }
      if source.supported_os:
        source_definition['supported_os'] = source.supported_os
      if source.conditions:
        source_definition['conditions'] = source.conditions
      if source.returned_types:
        source_definition['returned_types'] = source.returned_types
      sources.append(source_definition)

    artifact_definition = {
        'name': self.name,
        'doc': self.description,
        'sources': sources,
    }
    if self.labels:
      artifact_definition['labels'] = self.labels
    if self.supported_os:
      artifact_definition['supported_os'] = self.supported_os
    if self.provides:
      artifact_definition['provides'] = self.provides
    if self.conditions:
      artifact_definition['conditions'] = self.conditions
    if self.urls:
      artifact_definition['urls'] = self.urls
    return artifact_definition
