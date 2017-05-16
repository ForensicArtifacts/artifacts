# -*- coding: utf-8 -*-
"""Shared functions and classes for testing."""

import os
import shutil
import sys
import tempfile
import unittest


def skipUnlessHasTestFile(path_segments):
  """Decorator to skip a test if the test file does not exist.

  Args:
    path_segments (list[str]): path segments inside the test data directory.

  Returns:
    function: to invoke.
  """
  fail_unless_has_test_file = getattr(
      unittest, u'fail_unless_has_test_file', False)

  path = os.path.join(u'test_data', *path_segments)
  if fail_unless_has_test_file or os.path.exists(path):
    return lambda function: function

  if sys.version_info[0] < 3:
    path = path.encode(u'utf-8')

  # Note that the message should be of type str which is different for
  # different versions of Python.
  return unittest.skip('missing test file: {0:s}'.format(path))


def GetTestFilePath(path_segments):
  """Retrieves the path of a test file in the test data directory.

  Args:
    path_segments (list[str]): path segments inside the test data directory.

  Returns:
    str: path of the test file.
  """
  # Note that we need to pass the individual path segments to os.path.join
  # and not a list.
  return os.path.join(os.getcwd(), u'test_data', *path_segments)


class BaseTestCase(unittest.TestCase):
  """The base test case."""

  _DATA_PATH = os.path.join(os.getcwd(), u'data')
  _TEST_DATA_PATH = os.path.join(os.getcwd(), u'test_data')

  # Show full diff results, part of TestCase so does not follow our naming
  # conventions.
  maxDiff = None

  def _GetTestFilePath(self, path_segments):
    """Retrieves the path of a test file in the test data directory.

    Args:
      path_segments (list[str]): path segments inside the test data directory.

    Returns:
      str: path of the test file.
    """
    # Note that we need to pass the individual path segments to os.path.join
    # and not a list.
    return os.path.join(self._TEST_DATA_PATH, *path_segments)


class TempDirectory(object):
  """Class that implements a temporary directory."""

  def __init__(self):
    """Initializes a temporary directory."""
    super(TempDirectory, self).__init__()
    self.name = u''

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self.name = tempfile.mkdtemp()
    return self.name

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Make this work with the 'with' statement."""
    shutil.rmtree(self.name, True)
