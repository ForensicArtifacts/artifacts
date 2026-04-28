# -*- coding: utf-8 -*-
"""Tests for the source type objects."""

import unittest

from artifacts import errors
from artifacts import source_type

from tests import test_lib


class SourceTypeTest(test_lib.BaseTestCase):
  """Class to test the artifact source type."""


class ArtifactGroupSourceTypeTest(test_lib.BaseTestCase):
  """Class to test the artifact group source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.ArtifactGroupSourceType(names=['test'])


class FileSourceTypeTest(test_lib.BaseTestCase):
  """Class to test the files source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.FileSourceType(paths=['test'])
    source_type.FileSourceType(paths=['test'], separator='\\')

    with self.assertRaises(errors.FormatError):
      source_type.FileSourceType()

    with self.assertRaises(errors.FormatError):
      source_type.FileSourceType(paths='test')


class PathSourceTypeTest(test_lib.BaseTestCase):
  """Class to test the paths source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.PathSourceType(paths=['test'])
    source_type.PathSourceType(paths=['test'], separator='\\')

    with self.assertRaises(errors.FormatError):
      source_type.PathSourceType()

    with self.assertRaises(errors.FormatError):
      source_type.PathSourceType(paths='test')


class WindowsRegistryKeySourceTypeTest(test_lib.BaseTestCase):
  """Class to test the Windows Registry keys source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WindowsRegistryKeySourceType(keys=['HKEY_LOCAL_MACHINE\\test'])

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryKeySourceType(keys='HKEY_LOCAL_MACHINE\\test')


class WindowsRegistryValueSourceTypeTest(test_lib.BaseTestCase):
  """Class to test the Windows Registry value source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    key_value_pair = {'key': 'HKEY_LOCAL_MACHINE\\test', 'value': 'test'}
    source_type.WindowsRegistryValueSourceType(key_value_pairs=[key_value_pair])

    key_value_pair = {'bad': 'test', 'value': 'test'}
    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(
          key_value_pairs=[key_value_pair])

    with self.assertRaises(errors.FormatError):
      source_type.WindowsRegistryValueSourceType(key_value_pairs=key_value_pair)


class WMIQuerySourceTypeTest(test_lib.BaseTestCase):
  """Class to test the WMI query source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WMIQuerySourceType(query='test')


class SourceTypeFactoryTest(test_lib.BaseTestCase):
  """Class to test the source type factory."""

  def testCreateSourceType(self):
    """Tests the source type creation."""
    source_type.SourceTypeFactory.RegisterSourceTypes([test_lib.TestSourceType])

    with self.assertRaises(KeyError):
      source_type.SourceTypeFactory.RegisterSourceTypes([
          test_lib.TestSourceType])

    source_object = source_type.SourceTypeFactory.CreateSourceType(
        'test', {'test': 'test123'})

    self.assertIsNotNone(source_object)
    self.assertEqual(source_object.test, 'test123')

    with self.assertRaises(errors.FormatError):
      source_object = source_type.SourceTypeFactory.CreateSourceType(
          'test', {})

    with self.assertRaises(errors.FormatError):
      source_object = source_type.SourceTypeFactory.CreateSourceType(
          'bogus', {})

    source_type.SourceTypeFactory.DeregisterSourceType(test_lib.TestSourceType)

  def testRegisterSourceType(self):
    """Tests the source type registration functions."""
    expected_number_of_source_types = len(
        source_type.SourceTypeFactory.GetSourceTypes())

    source_type.SourceTypeFactory.RegisterSourceType(test_lib.TestSourceType)

    number_of_source_types = len(source_type.SourceTypeFactory.GetSourceTypes())
    self.assertEqual(
        number_of_source_types, expected_number_of_source_types + 1)

    source_type.SourceTypeFactory.DeregisterSourceType(test_lib.TestSourceType)

    number_of_source_types = len(source_type.SourceTypeFactory.GetSourceTypes())
    self.assertEqual(number_of_source_types, expected_number_of_source_types)

  def testRegisterSourceTypeRaisesWhenAlreadyRegistered(self):
    """Tests the source type registration functions when already registered."""
    source_type.SourceTypeFactory.RegisterSourceType(test_lib.TestSourceType)

    with self.assertRaises(KeyError):
      source_type.SourceTypeFactory.RegisterSourceType(test_lib.TestSourceType)

    source_type.SourceTypeFactory.DeregisterSourceType(test_lib.TestSourceType)


if __name__ == '__main__':
  unittest.main()
