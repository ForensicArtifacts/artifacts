# -*- coding: utf-8 -*-
"""Tests for the source type objects."""

import unittest

from artifacts import errors
from artifacts import source_type


class SourceTypeTest(unittest.TestCase):
  """Class to test the artifact source type."""


class ArtifactGroupSourceTypeTest(unittest.TestCase):
  """Class to test the artifact group source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.ArtifactGroupSourceType(names=[u'test'])


class FileSourceTypeTest(unittest.TestCase):
  """Class to test the files source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.FileSourceType(paths=[u'test'])
    source_type.FileSourceType(paths=[u'test'], separator=u'\\')


class PathSourceTypeTest(unittest.TestCase):
  """Class to test the paths source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.PathSourceType(paths=[u'test'])
    source_type.PathSourceType(paths=[u'test'], separator=u'\\')


class WindowsRegistryKeySourceTypeTest(unittest.TestCase):
  """Class to test the Windows Registry keys source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WindowsRegistryKeySourceType(keys=[u'HKEY_LOCAL_MACHINE\\test'])

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryKeySourceType(keys=u'HKEY_LOCAL_MACHINE\\test')


class WindowsRegistryValueSourceTypeTest(unittest.TestCase):
  """Class to test the Windows Registry value source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    key_value_pair = {'key': u'HKEY_LOCAL_MACHINE\\test', 'value': u'test'}
    source_type.WindowsRegistryValueSourceType(key_value_pairs=[key_value_pair])

    key_value_pair = {'bad': u'test', 'value': u'test'}
    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(
          key_value_pairs=[key_value_pair])

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(key_value_pairs=key_value_pair)


class WMIQuerySourceType(unittest.TestCase):
  """Class to test the WMI query source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WMIQuerySourceType(query=u'test')


if __name__ == '__main__':
  unittest.main()
