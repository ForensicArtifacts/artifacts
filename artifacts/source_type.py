#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The source type objects.

The source type objects define the source of the artifact data. In earlier
versions of the artifact defintions collector definitions had a similar
purpose as the source type. Currently the following source types are defined:
* artifact; the source is one or more artifact definitions;
* file; the source is one or more files;
* path; the source is one or more paths;
* Windows Registry key; the source is one or more Windows Registry keys;
* Windows Registry value; the source a Windows Registry value;
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

  def __init__(self, **kwargs):
    """Initializes the source type object.

    Args:
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when there are unused keyword arguments.
    """
    if kwargs:
      raise errors.FormatError(u'Unused keyword arguments.')

    super(SourceType, self).__init__()

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


class ArtifactSourceType(SourceType):
  """Class that implements the artifacts source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_ARTIFACT

  def __init__(self, artifact_names=None, **kwargs):
    """Initializes the source type object.

    Args:
      artifact_names: optional list of artifact definition names.
                      The default is None.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when artifact names is not set.
    """
    if not artifact_names:
      raise errors.FormatError(u'Missing artifact names value.')

    super(ArtifactSourceType, self).__init__(**kwargs)
    self.artifact_names = artifact_names


class FileSourceType(SourceType):
  """Class that implements the file source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_FILE

  def __init__(self, locations=None, separator=u'/', **kwargs):
    """Initializes the source type object.

    Args:
      locations: optional list of location strings. The locations are
                 considered relative to the root of the file system.
                 The default is None.
      separator: optional string containing the path segment separator.
                 The default is /.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when locations is not set.
    """
    if not locations:
      raise errors.FormatError(u'Missing locations value.')

    super(FileSourceType, self).__init__(**kwargs)
    self.locations = locations
    self.separator = separator


class PathSourceType(SourceType):
  """Class that implements the path source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_PATH

  def __init__(self, locations=None, separator=u'/', **kwargs):
    """Initializes the source type object.

    Args:
      locations: optional list of location strings. The locations are
                 considered relative to the root of the file system.
                 The default is None.
      separator: optional string containing the path segment separator.
                 The default is /.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when locations is not set.
    """
    if not locations:
      raise errors.FormatError(u'Missing locations value.')

    super(PathSourceType, self).__init__(**kwargs)
    self.locations = locations
    self.separator = separator


class WindowsRegistryKeySourceType(SourceType):
  """Class that implements the Windows Registry key source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_KEY

  def __init__(self, keys=None, **kwargs):
    """Initializes the source type object.

    Args:
      keys: optional list of key paths. The default is None.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when keys is not set.
    """
    if not keys:
      raise errors.FormatError(u'Missing keys value.')

    super(WindowsRegistryKeySourceType, self).__init__(**kwargs)
    self.keys = keys


class WindowsRegistryValueSourceType(SourceType):
  """Class that implements the Windows Registry value source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WINDOWS_REGISTRY_VALUE

  def __init__(self, key=None, value=None, **kwargs):
    """Initializes the source type object.

    Args:
      key: optional path of the key. The default is None.
      value: optional name of the value. The default is None.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when key or value are not set.
    """
    if not key or not value:
      raise errors.FormatError(u'Missing key or value value.')

    super(WindowsRegistryValueSourceType, self).__init__(**kwargs)
    self.key = key
    self.value = value


class WMIQuerySourceType(SourceType):
  """Class that implements the WMI query source type."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_WMI_QUERY

  def __init__(self, query=None, **kwargs):
    """Initializes the source type object.

    Args:
      query: optional string containing the WMI query. The default is None.
      kwargs: a dictionary of keyword arguments dependending on
              the source type.

    Raises:
      FormatError: when query is not set.
    """
    if not query:
      raise errors.FormatError(u'Missing query value.')

    super(WMIQuerySourceType, self).__init__(**kwargs)
    self.query = query
