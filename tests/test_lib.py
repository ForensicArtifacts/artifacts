"""Shared functions and classes for testing."""

import os
import shutil
import tempfile
import unittest

from artifacts import errors
from artifacts import source_type


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

    super().__init__()
    self.test = test

  def AsDict(self):
    """Represents a source type as a dictionary.

    Returns:
      dict[str, str]: source type attributes.
    """
    return {'test': self.test}


class BaseTestCase(unittest.TestCase):
  """The base test case."""

  _DATA_PATH = os.path.join(os.getcwd(), 'artifacts', 'data')
  _TEST_DATA_PATH = os.path.join(os.getcwd(), 'test_data')

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

  def _SkipIfPathNotExists(self, path):
    """Skips the test if the path does not exist.

    Args:
      path (str): path of a test file.

    Raises:
      SkipTest: if the path path does not exist and the test should be skipped.
    """
    if not os.path.exists(path):
      filename = os.path.basename(path)
      raise unittest.SkipTest(f'missing test file: {filename:s}')


class TempDirectory:
  """Class that implements a temporary directory."""

  def __init__(self):
    """Initializes a temporary directory."""
    super().__init__()
    self.name = ''

  def __enter__(self):
    """Make this work with the 'with' statement."""
    self.name = tempfile.mkdtemp()
    return self.name

  def __exit__(self, unused_type, unused_value, unused_traceback):
    """Make this work with the 'with' statement."""
    shutil.rmtree(self.name, True)
