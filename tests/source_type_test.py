# -*- coding: utf-8 -*-
"""Tests for the source type objects."""

import unittest

from artifacts import errors
from artifacts import source_type

from tests import test_lib


class TestSourceType(source_type.SourceType):
  """Class that implements a test source type."""

  TYPE_INDICATOR = 'test'

  def __init__(self, test=None):
    """Initializes the source type object.

    Args:
      test (Optional[str]): test string.

    Raises:
      FormatError: when test is not set.
    """
    if not test:
      raise errors.FormatError('Missing test value.')

    super(TestSourceType, self).__init__()
    self.test = test

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'test': self.test}


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
    source_type.SourceTypeFactory.RegisterSourceTypes([TestSourceType])

    with self.assertRaises(KeyError):
      source_type.SourceTypeFactory.RegisterSourceTypes([TestSourceType])

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

    source_type.SourceTypeFactory.DeregisterSourceType(TestSourceType)

  def testRegisterSourceType(self):
    """Tests the source type registration functions."""
    expected_number_of_source_types = len(
        source_type.SourceTypeFactory.GetSourceTypes())

    source_type.SourceTypeFactory.RegisterSourceType(TestSourceType)

    number_of_source_types = len(source_type.SourceTypeFactory.GetSourceTypes())
    self.assertEqual(
        number_of_source_types, expected_number_of_source_types + 1)

    source_type.SourceTypeFactory.DeregisterSourceType(TestSourceType)

    number_of_source_types = len(source_type.SourceTypeFactory.GetSourceTypes())
    self.assertEqual(number_of_source_types, expected_number_of_source_types)

  def testRegisterSourceTypeRaisesWhenAlreadyRegistered(self):
    """Tests the source type registration functions when already registered."""
    source_type.SourceTypeFactory.RegisterSourceType(TestSourceType)

    with self.assertRaises(KeyError):
      source_type.SourceTypeFactory.RegisterSourceType(TestSourceType)

    source_type.SourceTypeFactory.DeregisterSourceType(TestSourceType)


if __name__ == '__main__':
  unittest.main()
