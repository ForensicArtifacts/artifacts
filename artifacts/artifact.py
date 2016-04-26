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

    source_type_class = None
    if type_indicator == definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
      source_type_class = source_type.ArtifactGroupSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_COMMAND:
      source_type_class = source_type.CommandSourceType

    elif type_indicator == definitions.TYPE_INDICATOR_COMMAND:
      source_type_class = source_type.CommandCollectorDefinition

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
      raise errors.FormatError(
          u'Unsupported type indicator: {0}.'.format(type_indicator))

    try:
      source_object = source_type_class(**attributes)
    except (TypeError, AttributeError) as e:
      raise errors.FormatError(
          "Invalid artifact definition for {0}: {1}".format(self.name, e))

    self.sources.append(source_object)
    return source_object
