# -*- coding: utf-8 -*-
r"""The source type objects.

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
artifact definition, pointing to a location e.g. C:\Windows. And where
C:\Windows\System32\winevt\Logs\AppEvent.evt a file artifact definition,
pointing to the Application Event Log file.
"""

import abc

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
      raise NotImplementedError(u'Invalid source type missing type indicator.')
    return self.TYPE_INDICATOR

  @abc.abstractmethod
  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """


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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {u'names': self.names}


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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {u'paths': self.paths}
    if self.separator != u'/':
      source_type_attributes[u'separator'] = self.separator

    return source_type_attributes


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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {u'cmd': self.cmd, u'args': self.args}


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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {u'paths': self.paths}
    if self.separator != u'/':
      source_type_attributes[u'separator'] = self.separator

    return source_type_attributes


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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {u'paths': self.paths}
    if self.separator != u'/':
      source_type_attributes[u'separator'] = self.separator

    return source_type_attributes


class WindowsRegistryKeySourceType(SourceType):
  """Class that implements the Windows Registry key source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY

  VALID_PREFIXES = [
      r'HKEY_LOCAL_MACHINE',
      r'HKEY_USERS',
      r'HKEY_CLASSES_ROOT',
      r'%%current_control_set%%',]

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

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {u'keys': self.keys}

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
      if set(pair.keys()) != set([u'key', u'value']):
        error_message = (
            u'key_value_pair missing "key" and "value" keys, got: {0}'
        ).format(key_value_pairs)
        raise errors.FormatError(error_message)
      WindowsRegistryKeySourceType.ValidateKey(pair['key'])

    super(WindowsRegistryValueSourceType, self).__init__()
    self.key_value_pairs = key_value_pairs

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {u'key_value_pairs': self.key_value_pairs}


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
    self.base_object = base_object
    self.query = query

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    source_type_attributes = {u'query': self.query}
    if self.base_object:
      source_type_attributes[u'base_object'] = self.base_object

    return source_type_attributes


class SourceTypeFactory(object):
  """Class that implements a source type factory."""

  _source_type_classes = {
      definitions.TYPE_INDICATOR_ARTIFACT_GROUP:
          ArtifactGroupSourceType,
      definitions.TYPE_INDICATOR_COMMAND:
          CommandSourceType,
      definitions.TYPE_INDICATOR_DIRECTORY:
          DirectorySourceType,
      definitions.TYPE_INDICATOR_FILE:
          FileSourceType,
      definitions.TYPE_INDICATOR_PATH:
          PathSourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY:
          WindowsRegistryKeySourceType,
      definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE:
          WindowsRegistryValueSourceType,
      definitions.TYPE_INDICATOR_WMI_QUERY:
          WMIQuerySourceType,}

  @classmethod
  def CreateSourceType(cls, type_indicator, attributes):
    """Creates a source type object.

    Args:
      type_indicator: the source type indicator.
      attributes: a dictionary containing the source attributes.

    Returns:
      A source type object (instance of SourceType).

    Raises:
      The source type object (instance of SourceType) or None if the type
      indicator is not supported.

    Raises:
      FormatError: if the type indicator is not set or unsupported,
                   or if required attributes are missing.
    """
    if type_indicator not in cls._source_type_classes:
      raise errors.FormatError(
          u'Unsupported type indicator: {0}.'.format(type_indicator))

    return cls._source_type_classes[type_indicator](**attributes)

  @classmethod
  def DeregisterSourceType(cls, source_type_class):
    """Deregisters a source type.

    The source types are identified based on their type indicator.

    Args:
      source_type_class: the source type (subclass of SourceType).

    Raises:
      KeyError: if a source type is not set for the corresponding type
                indicator.
    """
    if source_type_class.TYPE_INDICATOR not in cls._source_type_classes:
      raise KeyError(
          u'Source type not set for type: {0}.'.format(
              source_type_class.TYPE_INDICATOR))

    del cls._source_type_classes[source_type_class.TYPE_INDICATOR]

  @classmethod
  def GetSourceTypes(cls):
    """Retrieves the source types.

    Returns:
      A list of source types (subclasses of SourceType).
    """
    return cls._source_type_classes.values()

  @classmethod
  def GetSourceTypeIndicators(cls):
    """Retrieves the source type indicators.

    Returns:
      A list of source type indicators.
    """
    return cls._source_type_classes.keys()

  @classmethod
  def RegisterSourceType(cls, source_type_class):
    """Registers a source type.

    The source types are identified based on their type indicator.

    Args:
      source_type_class: the source type (subclass of SourceType).

    Raises:
      KeyError: if source types is already set for the corresponding
                type indicator.
    """
    if source_type_class.TYPE_INDICATOR in cls._source_type_classes:
      raise KeyError(
          u'Source type already set for type: {0}.'.format(
              source_type_class.TYPE_INDICATOR))

    cls._source_type_classes[source_type_class.TYPE_INDICATOR] = (
        source_type_class)

  @classmethod
  def RegisterSourceTypes(cls, source_type_classes):
    """Registers source types.

    The source types are identified based on their type indicator.

    Args:
      source_type_classes: a list of source types (instances of SourceType).
    """
    for source_type_class in source_type_classes:
      cls.RegisterSourceType(source_type_class)
