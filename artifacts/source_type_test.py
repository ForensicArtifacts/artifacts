#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the source type objects."""

import unittest

from artifacts import errors
from artifacts import source_type


class SourceTypeTest(unittest.TestCase):
  """Class to test the artifact source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    with self.assertRaises(errors.FormatError):
      source_type.SourceType(bogus=u'bogus')


class ArtifactSourceTypeTest(unittest.TestCase):
  """Class to test the artifacts source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.ArtifactSourceType(artifact_names=[u'test'])

    with self.assertRaises(errors.FormatError):
      source_type.ArtifactSourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.ArtifactSourceType(artifact_names=[u'test'], bogus=u'bogus')


class FileSourceTypeTest(unittest.TestCase):
  """Class to test the files source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.FileSourceType(locations=[u'test'])
    source_type.FileSourceType(locations=[u'test'], separator=u'\\')

    with self.assertRaises(errors.FormatError):
      source_type.FileSourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.FileSourceType(locations=[u'test'], bogus=u'bogus')


class PathSourceTypeTest(unittest.TestCase):
  """Class to test the paths source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.PathSourceType(locations=[u'test'])
    source_type.PathSourceType(locations=[u'test'], separator=u'\\')

    with self.assertRaises(errors.FormatError):
      source_type.PathSourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.PathSourceType(locations=[u'test'], bogus=u'bogus')


class WindowsRegistryKeySourceTypeTest(unittest.TestCase):
  """Class to test the Windows Registry keys source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WindowsRegistryKeySourceType(keys=[u'test'])

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryKeySourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryKeySourceType(keys=[u'test'], bogus=u'bogus')


class WindowsRegistryValueSourceTypeTest(unittest.TestCase):
  """Class to test the Windows Registry value source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WindowsRegistryValueSourceType(key=u'test', value=u'test')

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(key=u'test')

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(value=u'test')

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(
          key=u'test', value=u'test', bogus=u'bogus')


class WMIQuerySourceType(unittest.TestCase):
  """Class to test the WMI query source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WMIQuerySourceType(query=u'test')

    with self.assertRaises(errors.FormatError):
      source_type.WMIQuerySourceType(bogus=u'bogus')

    with self.assertRaises(errors.FormatError):
      source_type.WMIQuerySourceType(query=u'test', bogus=u'bogus')


if __name__ == '__main__':
  unittest.main()
