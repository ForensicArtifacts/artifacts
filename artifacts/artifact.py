# -*- coding: utf-8 -*-
"""The reader objects."""

from artifacts import definitions
from artifacts import errors
from artifacts import registry
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

    try:
      source_object = registry.ArtifactDefinitionsRegistry.CreateSourceType(
          type_indicator, attributes)
    except (AttributeError, TypeError) as exception:
      raise errors.FormatError(
          u'Invalid artifact definition for {0}: {1}'.format(self.name,
                                                             exception))

    self.sources.append(source_object)
    return source_object
