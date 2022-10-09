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

import abc

from artifacts import definitions
from artifacts import errors


class SourceType(object):
  """Artifact definition source type interface."""

  # Note that redundant-returns-doc is broken for pylint 1.7.x for
  # abstract methods.
  # pylint: disable=redundant-returns-doc

  TYPE_INDICATOR = None

  def __init__(self):
    """Initializes an artifact definition source type.

    Raises:
      FormatError: if the indicator is not defined.
    """
    super(SourceType, self).__init__()

    if not self.TYPE_INDICATOR:
      raise errors.FormatError('Missing type indicator.')

  @property
  def type_indicator(self):
    """str: type indicator."""
    return self.TYPE_INDICATOR

  @abc.abstractmethod
  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """


class ArtifactGroupSourceType(SourceType):
  """Artifact group source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_ARTIFACT_GROUP

  def __init__(self, names=None):
    """Initializes a source type.

    Args:
      names (Optional[str]): artifact definition names.

    Raises:
      FormatError: when artifact names is not set.
    """
    if not names:
      raise errors.FormatError('Missing names value.')

    super(ArtifactGroupSourceType, self).__init__()
    self.names = names

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'names': self.names}


class CommandSourceType(SourceType):
  """Command source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_COMMAND

  def __init__(self, args=None, cmd=None):
    """Initializes a source type.

    Args:
      args (list[str]): arguments to the command to run.
      cmd (str): command to run.

    Raises:
      FormatError: when args or cmd is not set.
    """
    if args is None or cmd is None:
      raise errors.FormatError('Missing args or cmd value.')

    super(CommandSourceType, self).__init__()
    self.args = args
    self.cmd = cmd

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'cmd': self.cmd, 'args': self.args}


class DirectorySourceType(SourceType):
  """Directory source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_DIRECTORY

  def __init__(self, paths=None, separator='/'):
    """Initializes a source type.

    Args:
      paths (Optional[str]): paths relative to the root of the file system.
      separator (Optional[str]): path segment separator.

    Raises:
      FormatError: when paths is not set or not a list type.
    """
    if not paths:
      raise errors.FormatError('Missing paths value.')

    if not isinstance(paths, list):
      raise errors.FormatError('Invalid paths value, not a list.')

    super(DirectorySourceType, self).__init__()
    self.paths = paths
    self.separator = separator

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {'paths': self.paths}
    if self.separator != '/':
      source_type_attributes['separator'] = self.separator

    return source_type_attributes


class FileSourceType(SourceType):
  """File source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_FILE

  def __init__(self, paths=None, separator='/'):
    """Initializes a source type.

    Args:
      paths (Optional[str]): paths relative to the root of the file system.
      separator (Optional[str]): path segment separator.

    Raises:
      FormatError: when paths is not set or not a list type.
    """
    if not paths:
      raise errors.FormatError('Missing paths value.')

    if not isinstance(paths, list):
      raise errors.FormatError('Invalid paths value, not a list.')

    super(FileSourceType, self).__init__()
    self.paths = paths
    self.separator = separator

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {'paths': self.paths}
    if self.separator != '/':
      source_type_attributes['separator'] = self.separator

    return source_type_attributes


class PathSourceType(SourceType):
  """Path source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_PATH

  def __init__(self, paths=None, separator='/'):
    """Initializes a source type.

    Args:
      paths (Optional[str]): paths relative to the root of the file system.
      separator (Optional[str]): path segment separator.

    Raises:
      FormatError: when paths is not set or not a list type.
    """
    if not paths:
      raise errors.FormatError('Missing paths value.')

    if not isinstance(paths, list):
      raise errors.FormatError('Invalid paths value, not a list.')

    super(PathSourceType, self).__init__()
    self.paths = paths
    self.separator = separator

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {'paths': self.paths}
    if self.separator != '/':
      source_type_attributes['separator'] = self.separator

    return source_type_attributes


class WindowsRegistryKeySourceType(SourceType):
  """Windows Registry key source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY

  VALID_PREFIXES = [
      r'HKEY_LOCAL_MACHINE',
      r'HKEY_USERS',
      r'HKEY_CLASSES_ROOT',
      r'%%current_control_set%%',
  ]

  def __init__(self, keys=None):
    """Initializes a source type.

    Args:
      keys (Optional[list[str]]): key paths relative to the root of
          the Windows Registry.

    Raises:
      FormatError: when keys is not set.
    """
    if not keys:
      raise errors.FormatError('Missing keys value.')

    if not isinstance(keys, list):
      raise errors.FormatError('keys must be a list')

    for key in keys:
      self.ValidateKey(key)

    super(WindowsRegistryKeySourceType, self).__init__()
    self.keys = keys

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'keys': self.keys}

  @classmethod
  def ValidateKey(cls, key_path):
    """Validates this key against supported key names.

    Args:
      key_path (str): path of a Windows Registry key.

    Raises:
      FormatError: when key is not supported.
    """
    for prefix in cls.VALID_PREFIXES:
      if key_path.startswith(prefix):
        return

    # TODO: move check to validator.
    if key_path.startswith('HKEY_CURRENT_USER\\'):
      raise errors.FormatError(
          'HKEY_CURRENT_USER\\ is not supported instead use: '
          'HKEY_USERS\\%%users.sid%%\\')

    raise errors.FormatError(f'Unupported Registry key path: {key_path:s}')


class WindowsRegistryValueSourceType(SourceType):
  """Windows Registry value source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE

  def __init__(self, key_value_pairs=None):
    """Initializes a source type.

    Args:
      key_value_pairs (Optional[list[tuple[str, str]]]): key path and value
          name pairs, where key paths are relative to the root of the Windows
          Registry.

    Raises:
      FormatError: when key value pairs is not set.
    """
    if not key_value_pairs:
      raise errors.FormatError('Missing key value pairs value.')

    if not isinstance(key_value_pairs, list):
      raise errors.FormatError('key_value_pairs must be a list')

    for pair in key_value_pairs:
      if not isinstance(pair, dict):
        raise errors.FormatError('key_value_pair must be a dict')

      if set(pair.keys()) != set(['key', 'value']):
        key_value_pairs = ', '.join([
            f'{key:s}: {value:s}' for key, value in key_value_pairs])
        raise errors.FormatError((
            f'key_value_pair missing "key" and "value" keys, got: '
            f'{key_value_pairs:s}'))

      WindowsRegistryKeySourceType.ValidateKey(pair['key'])

    super(WindowsRegistryValueSourceType, self).__init__()
    self.key_value_pairs = key_value_pairs

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'key_value_pairs': self.key_value_pairs}


class WMIQuerySourceType(SourceType):
  """WMI query source type.

  Attributes:
    base_object (str): WMI base object.
    query (str): WMI query.
  """

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WMI_QUERY

  def __init__(self, base_object=None, query=None):
    """Initializes a source type.

    Args:
      base_object (Optional[str]): WMI base object.
      query (Optional[str]): WMI query.

    Raises:
      FormatError: when query is not set.
    """
    if not query:
      raise errors.FormatError('Missing query value.')

    super(WMIQuerySourceType, self).__init__()
    self.base_object = base_object
    self.query = query

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {'query': self.query}
    if self.base_object:
      source_type_attributes['base_object'] = self.base_object

    return source_type_attributes


class SourceTypeFactory(object):
  """Source type factory."""

  _source_type_classes = {
      definitions.TYPE_INDICATOR_ARTIFACT_GROUP: ArtifactGroupSourceType,
      definitions.TYPE_INDICATOR_COMMAND: CommandSourceType,
      definitions.TYPE_INDICATOR_DIRECTORY: DirectorySourceType,
      definitions.TYPE_INDICATOR_FILE: FileSourceType,
      definitions.TYPE_INDICATOR_PATH: PathSourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
          WindowsRegistryKeySourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
          WindowsRegistryValueSourceType,
      definitions.TYPE_INDICATOR_WMI_QUERY: WMIQuerySourceType,
  }

  @classmethod
  def CreateSourceType(cls, type_indicator, attributes):
    """Creates a source type.

    Args:
      type_indicator (str): source type indicator.
      attributes (dict[str, object]): source type attributes.

    Returns:
      SourceType: a source type.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
          or if required attributes are missing.
    """
    if type_indicator not in cls._source_type_classes:
      raise errors.FormatError(
          f'Unsupported type indicator: {type_indicator:s}.')

    return cls._source_type_classes[type_indicator](**attributes)

  @classmethod
  def DeregisterSourceType(cls, source_type_class):
    """Deregisters a source type.

    Source types are identified based on their type indicator.

    Args:
      source_type_class (type): source type.

    Raises:
      KeyError: if a source type is not set for the corresponding type
          indicator.
    """
    if source_type_class.TYPE_INDICATOR not in cls._source_type_classes:
      raise KeyError((
          f'Source type not set for type: '
          f'{source_type_class.TYPE_INDICATOR:s}.'))

    del cls._source_type_classes[source_type_class.TYPE_INDICATOR]

  @classmethod
  def GetSourceTypes(cls):
    """Retrieves the source types.

    Returns:
      list[type]: source types.
    """
    return cls._source_type_classes.values()

  @classmethod
  def GetSourceTypeIndicators(cls):
    """Retrieves the source type indicators.

    Returns:
      list[str]: source type indicators.
    """
    return cls._source_type_classes.keys()

  @classmethod
  def RegisterSourceType(cls, source_type_class):
    """Registers a source type.

    Source types are identified based on their type indicator.

    Args:
      source_type_class (type): source type.

    Raises:
      KeyError: if source types is already set for the corresponding
          type indicator.
    """
    if source_type_class.TYPE_INDICATOR in cls._source_type_classes:
      raise KeyError((
          f'Source type already set for type: '
          f'{source_type_class.TYPE_INDICATOR:s}.'))

    cls._source_type_classes[source_type_class.TYPE_INDICATOR] = (
        source_type_class)

  @classmethod
  def RegisterSourceTypes(cls, source_type_classes):
    """Registers source types.

    Source types are identified based on their type indicator.

    Args:
      source_type_classes (list[type]): source types.
    """
    for source_type_class in source_type_classes:
      cls.RegisterSourceType(source_type_class)
