# -*- coding: utf-8 -*-
"""Tests for the source type objects."""

import unittest

from artifacts import errors
from artifacts import source_type


class TestSourceType(source_type.SourceType):
  """Class that implements a test source type."""

  TYPE_INDICATOR = u'test'

  def __init__(self, test=None):
    """Initializes the source type object.

    Args:
      test: optional test string. The default is None.

    Raises:
      FormatError: when test is not set.
    """
    if not test:
      raise errors.FormatError(u'Missing test value.')

    super(TestSourceType, self).__init__()
    self.test = test

  def CopyToDict(self):
    """Copies the source type to a dictionary.

    Returns:
      A dictionary containing the source type attributes.
    """
    return {u'test': self.test}


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


class WMIQuerySourceTypeTest(unittest.TestCase):
  """Class to test the WMI query source type."""

  def testInitialize(self):
    """Tests the __init__ function."""
    source_type.WMIQuerySourceType(query=u'test')


class SourceTypeFactoryTest(unittest.TestCase):
  """Class to test the source type factory."""

  def testCreateSourceType(self):
    """Tests the source type creation."""
    source_type.SourceTypeFactory.RegisterSourceTypes([TestSourceType])

    with self.assertRaises(KeyError):
      source_type.SourceTypeFactory.RegisterSourceTypes([TestSourceType])

    source_object = source_type.SourceTypeFactory.CreateSourceType(
        u'test', {u'test': u'test123'})

    self.assertIsNotNone(source_object)
    self.assertEqual(source_object.test, u'test123')

    with self.assertRaises(errors.FormatError):
      source_object = source_type.SourceTypeFactory.CreateSourceType(u'test',
                                                                     {})

    with self.assertRaises(errors.FormatError):
      source_object = source_type.SourceTypeFactory.CreateSourceType(u'bogus',
                                                                     {})

    source_type.SourceTypeFactory.DeregisterSourceType(TestSourceType)

  def testRegisterSourceType(self):
    """Tests the source type registration functions."""
    expected_number_of_source_types = len(
        source_type.SourceTypeFactory.GetSourceTypes())

    source_type.SourceTypeFactory.RegisterSourceType(TestSourceType)

    number_of_source_types = len(source_type.SourceTypeFactory.GetSourceTypes())
    self.assertEqual(number_of_source_types,
                     expected_number_of_source_types + 1)

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
