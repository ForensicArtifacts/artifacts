#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The ForensicArtifacts.com Artifact Repository project.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The reader objects."""

from artifacts import collector
from artifacts import definitions


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
    self.supported_os = []
    self.urls = []

  # Property for name compatibility with current variant of GRR artifacts.
  @property
  def doc(self):
    """The documentation string."""
    return self.description

  def AppendCollector(self, type_indicator, attributes):
    """Appends a collector definition.

    This function ignores unsupported collector type indicators.

    Args:
      type_indicator: the collector type indicator.
      attributes: a dictionary containing the collector attributes.

    Returns:
      The collector definition object (instance of CollectorDefinition) or
      None if the type indicator is not supported.

    Raises:
      ValueError: if the type indicator is invalid or if required attributes
                  are missing.
    """
    if not type_indicator:
      raise ValueError(u'Invalid type indicator.')

    collector_class = None
    if type_indicator == definitions.TYPE_INDICATOR_ARTIFACT:
      collector_class = collector.ArtifactCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_FILE:
      collector_class = collector.FileCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
      collector_class = collector.WindowsRegistryKeyCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
      collector_class = collector.WindowsRegistryValueCollectorDefinition

    elif type_indicator == definitions.TYPE_INDICATOR_WMI_QUERY:
      collector_class = collector.WMIQueryCollectorDefinition

    if collector_class:
      collector_definition = collector_class(**attributes)
      self.collectors.append(collector_definition)
    else:
      collector_definition = None

    return collector_definition
