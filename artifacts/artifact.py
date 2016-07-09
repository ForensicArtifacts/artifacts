# -*- coding: utf-8 -*-
"""The reader objects."""

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
