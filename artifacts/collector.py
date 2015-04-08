# -*- coding: utf-8 -*-
"""The collector definition objects.

These classes allow us to validate artifact definitions by instantiating them
as objects. For your implementation you want to likely implement collector
objects that actual collect files, Windows Registry values, etc.
"""

from artifacts import definitions
from artifacts import errors


class CollectorDefinition(object):
  """Class that implements the collector definition interface."""

  TYPE_INDICATOR = None

  def __init__(self):
    """Initializes the collector definition object."""
    super(CollectorDefinition, self).__init__()
    self.conditions = []
    self.returned_types = []
    self.supported_os = []

  @property
  def type_indicator(self):
    """The type indicator."""
    type_indicator = getattr(self, 'TYPE_INDICATOR', None)
    if type_indicator is None:
      raise NotImplementedError(
          u'Invalid path specification missing type indicator.')
    return type_indicator


class ArtifactCollectorDefinition(CollectorDefinition):
  """Class that implements the artifact collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_ARTIFACT

  def __init__(self, artifact_list=None):
    """Initializes the collector definition object.

    Args:
      artifact_list: optional list of artifact definition names.
                     The default is None.
    Raises:
      FormatError: when artifact_list is not set.
    """
    if not artifact_list:
      raise errors.FormatError(u'Missing artifact_list value.')

    super(ArtifactCollectorDefinition, self).__init__()
    self.artifact_list = artifact_list


class CommandCollectorDefinition(CollectorDefinition):
  """Class that implements the command collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_COMMAND

  def __init__(self, args=None, cmd=None):
    """Initializes the collector definition object.

    Args:
      args: list of strings that will be passed as arguments to cmd.
      cmd: string representing the command to run.

    Raises:
      FormatError: when args or cmd is not set.
    """
    if args is None or cmd is None:
      raise errors.FormatError(u'Missing args or cmd value.')

    super(CommandCollectorDefinition, self).__init__()
    self.args = args
    self.cmd = cmd


class FileCollectorDefinition(CollectorDefinition):
  """Class that implements the file collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_FILE

  def __init__(self, path_list=None):
    """Initializes the collector definition object.

    Args:
      path_list: optional list of path strings. The default is None.

    Raises:
      FormatError: when path_list is not set.
    """
    if not path_list:
      raise errors.FormatError(u'Missing path_list value.')

    super(FileCollectorDefinition, self).__init__()
    self.path_list = path_list


class WindowsRegistryKeyCollectorDefinition(CollectorDefinition):
  """Class that implements the Windows Registry key collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY

  def __init__(self, path_list=None):
    """Initializes the collector definition object.

    Args:
      path_list: optional list of path strings. The default is None.

    Raises:
      FormatError: when path_list is not set.
    """
    if not path_list:
      raise errors.FormatError(u'Missing path_list value.')

    super(WindowsRegistryKeyCollectorDefinition, self).__init__()
    self.path_list = path_list


class WindowsRegistryValueCollectorDefinition(CollectorDefinition):
  """Class that implements the Windows Registry value collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE

  def __init__(self, path_list=None):
    """Initializes the collector definition object.

    Args:
      path_list: optional list of path strings. The default is None.

    Raises:
      FormatError: when path_list is not set.
    """
    if not path_list:
      raise errors.FormatError(u'Missing path_list value.')

    super(WindowsRegistryValueCollectorDefinition, self).__init__()
    self.path_list = path_list


class WMIQueryCollectorDefinition(CollectorDefinition):
  """Class that implements the WMI query collector definition."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WMI_QUERY

  def __init__(self, query=None):
    """Initializes the collector definition object.

    Args:
      query: optional string containing the WMI query. The default is None.

    Raises:
      FormatError: when query is not set.
    """
    if not query:
      raise errors.FormatError(u'Missing query value.')

    super(WMIQueryCollectorDefinition, self).__init__()
    self.query = query
