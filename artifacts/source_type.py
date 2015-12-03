# -*- coding: utf-8 -*-
"""The source type objects.

The source type objects define the source of the artifact data. In earlier
versions of the artifact definitions collector definitions had a similar
purpose as the source type. Currently the following source types are defined:
* artifact; the source is one or more artifact definitions;
* file; the source is one or more files;
* path; the source is one or more paths;
* Windows Registry key; the source is one or more Windows Registry keys;
* Windows Registry value; the source is one or more Windows Registry values;
* WMI query; the source is a Windows Management Instrumentation query.

The difference between the file and path source types are that file should
be used to define file entries that contain data and path, file entries that
define a location. E.g. on Windows %SystemRoot% could be considered a path
artifact definition, pointing to a location e.g. C:\\Windows. And where
C:\\Windows\\System32\\winevt\\Logs\\AppEvent.evt a file artifact definition,
pointing to the Application Event Log file.
"""

from artifacts import definitions
from artifacts import errors


class SourceType(object):
  """Class that implements the artifact definition source type interface."""

  TYPE_INDICATOR = None

  @property
  def type_indicator(self):
    """The type indicator.

    Raises:
      NotImplementedError: if the type indicator is not defined.
    """
    if not self.TYPE_INDICATOR:
      raise NotImplementedError(
          u'Invalid source type missing type indicator.')
    return self.TYPE_INDICATOR


class ArtifactGroupSourceType(SourceType):
  """Class that implements the artifact group source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_ARTIFACT_GROUP

  def __init__(self, names=None):
    """Initializes the source type object.

    Args:
      names: optional list of artifact definition names. The default is None.

    Raises:
      FormatError: when artifact names is not set.
    """
    if not names:
      raise errors.FormatError(u'Missing names value.')

    super(ArtifactGroupSourceType, self).__init__()
    self.names = names


class FileSourceType(SourceType):
  """Class that implements the file source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_FILE

  def __init__(self, paths=None, separator=u'/'):
    """Initializes the source type object.

    Args:
      paths: optional list of paths. The paths are considered relative
             to the root of the file system. The default is None.
      separator: optional string containing the path segment separator.
                 The default is /.

    Raises:
      FormatError: when paths is not set.
    """
    if not paths:
      raise errors.FormatError(u'Missing paths value.')

    super(FileSourceType, self).__init__()
    self.paths = paths
    self.separator = separator


class CommandSourceType(SourceType):
  """Class that implements the command source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_COMMAND

  def __init__(self, args=None, cmd=None):
    """Initializes the source type object.

    Args:
      args: list of strings that will be passed as arguments to the command.
      cmd: string representing the command to run.

    Raises:
      FormatError: when args or cmd is not set.
    """
    if args is None or cmd is None:
      raise errors.FormatError(u'Missing args or cmd value.')

    super(CommandSourceType, self).__init__()
    self.args = args
    self.cmd = cmd


class PathSourceType(SourceType):
  """Class that implements the path source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_PATH

  def __init__(self, paths=None, separator=u'/'):
    """Initializes the source type object.

    Args:
      paths: optional list of paths. The paths are considered relative
             to the root of the file system. The default is None.
      separator: optional string containing the path segment separator.
                 The default is /.

    Raises:
      FormatError: when paths is not set.
    """
    if not paths:
      raise errors.FormatError(u'Missing paths value.')

    super(PathSourceType, self).__init__()
    self.paths = paths
    self.separator = separator


class DirectorySourceType(SourceType):
  """Class that implements the directory source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_DIRECTORY

  def __init__(self, paths=None, separator=u'/'):
    """Initializes the source type object.

    Args:
      paths: optional list of paths. The paths are considered relative
             to the root of the file system. The default is None.
      separator: optional string containing the path segment separator.
                 The default is /.

    Raises:
      FormatError: when paths is not set.
    """
    if not paths:
      raise errors.FormatError(u'Missing directory value.')

    super(DirectorySourceType, self).__init__()
    self.paths = paths
    self.separator = separator


class WindowsRegistryKeySourceType(SourceType):
  """Class that implements the Windows Registry key source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY

  VALID_PREFIXES = [
      r'HKEY_LOCAL_MACHINE',
      r'HKEY_USERS',
      r'HKEY_CLASSES_ROOT',
      r'%%current_control_set%%',
  ]

  def __init__(self, keys=None):
    """Initializes the source type object.

    Args:
      keys: optional list of key paths. The key paths are considered relative
            to the root of the Windows Registry. The default is None.

    Raises:
      FormatError: when keys is not set.
    """
    if not keys:
      raise errors.FormatError(u'Missing keys value.')

    if not isinstance(keys, list):
      raise errors.FormatError(u'keys must be a list')

    for key in keys:
      self.ValidateKey(key)

    super(WindowsRegistryKeySourceType, self).__init__()
    self.keys = keys

  @classmethod
  def ValidateKey(cls, key_path):
    """Validates this key against supported key names.

    Args:
      key_path: string containing the path fo the Registry key.

    Raises:
      FormatError: when key is not supported.
    """
    for prefix in cls.VALID_PREFIXES:
      if key_path.startswith(prefix):
        return

    if key_path.startswith(u'HKEY_CURRENT_USER\\'):
      raise errors.FormatError(
          u'HKEY_CURRENT_USER\\ is not supported instead use: '
          u'HKEY_USERS\\%%users.sid%%\\')

    raise errors.FormatError(
        u'Unupported Registry key path: {0}'.format(key_path))


class WindowsRegistryValueSourceType(SourceType):
  """Class that implements the Windows Registry value source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE

  def __init__(self, key_value_pairs=None):
    """Initializes the source type object.

    Args:
      key_value_pairs: optional list of key path and value name pairs.
                       The key paths are considered relative to the root
                       of the Windows Registry. The default is None.

    Raises:
      FormatError: when key value pairs is not set.
    """
    if not key_value_pairs:
      raise errors.FormatError(u'Missing key value pairs value.')

    if not isinstance(key_value_pairs, list):
      raise errors.FormatError(u'key_value_pairs must be a list')

    for pair in key_value_pairs:
      if not isinstance(pair, dict):
        raise errors.FormatError(u'key_value_pair must be a dict')
      if set(pair.keys()) != set(['key', 'value']):
        raise errors.FormatError(u'key_value_pair missing "key" and "value"'
                                 u' keys, got: {}'.format(key_value_pairs))
      WindowsRegistryKeySourceType.ValidateKey(pair['key'])

    super(WindowsRegistryValueSourceType, self).__init__()
    self.key_value_pairs = key_value_pairs


class WMIQuerySourceType(SourceType):
  """Class that implements the WMI query source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WMI_QUERY

  def __init__(self, query=None, base_object=None):
    """Initializes the source type object.

    Args:
      query: optional string containing the WMI query. The default is None.

    Raises:
      FormatError: when query is not set.
    """
    if not query:
      raise errors.FormatError(u'Missing query value.')

    super(WMIQuerySourceType, self).__init__()
    self.query = query
    self.base_object = base_object
