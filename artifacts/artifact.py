#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The reader objects."""

from artifacts import collector
from artifacts import definitions
from artifacts import errors


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
    self.collectors = []
    self.conditions = []
    self.description = description
    self.name = name
    self.labels = []
    self.provides = []
    self.supported_os = []
    self.urls = []

  # Property for name compatibility with current variant of GRR artifacts.
  @property
  def doc(self):
    """The documentation string."""
    return self.description

  def AppendCollector(self, type_indicator, attributes):
    """Appends a collector definition.

    If you want to implement your own collector definition you should create
    a subclass in collector.py and change the AppendCollector method to
    handle the new subclass. This function raises FormatError if an unsupported
    collector type indicator is encountered.

    Args:
      type_indicator: the collector type indicator.
      attributes: a dictionary containing the collector attributes.

    Returns:
      The collector definition object (instance of CollectorDefinition) or
      None if the type indicator is not supported.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
                   or if required attributes are missing.
    """
    if not type_indicator:
      raise errors.FormatError(u'Missing type indicator.')

    collector_class = None
    if type_indicator == definitions.TYPE_INDICATOR_ARTIFACT:
      collector_class = collector.ArtifactCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_COMMAND:
      collector_class = collector.CommandCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_FILE:
      collector_class = collector.FileCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
      collector_class = collector.WindowsRegistryKeyCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
      collector_class = collector.WindowsRegistryValueCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WMI_QUERY:
      collector_class = collector.WMIQueryCollectorDefinition

    else:
      raise errors.FormatError(
          u'Unsupported type indicator: {0:s}.'.format(type_indicator))

    collector_definition = collector_class(**attributes)
    self.collectors.append(collector_definition)
    return collector_definition
