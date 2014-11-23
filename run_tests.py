#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 The ForensicArtifacts.com Artifact Repository project.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Script to run the tests."""

import glob
import os
import unittest
import sys


def FindTestFiles(path):
  """Find the test files (*_test.py) within the specified path."""
  file_list = []

  for directory, _, _ in os.walk(path):
    directory_pattern = os.path.join(directory, '*_test.py')

    for pattern_match in glob.iglob(directory_pattern):
      if os.path.isfile(pattern_match):
        file_list.append(pattern_match)

  return file_list


def RunTests(path_list):
  """Runs all the test for the test files found within the specified paths.

  Args:
    path_list: list of path string to look for test files.
  """
  test_classes = []

  for path in path_list:
    for test_file in FindTestFiles(path):
      library_name = (
          test_file.rstrip('.py').replace(os.path.sep, '.').lstrip('.'))
      test_classes.append(library_name)

  tests = unittest.TestLoader().loadTestsFromNames(test_classes)
  test_run = unittest.TextTestRunner(verbosity=1)
  return test_run.run(tests)


def FormatHeader(header, char='*'):
  """Format and return a header for output."""
  return ('\n{:%s^80}' % char).format(u' %s ' % header)


def PrintResults(my_results):
  """Print the results from an aggregated test run."""
  errors = 0
  failures = 0
  print 'Ran: {0:d} tests.'.format(my_results.testsRun)

  if my_results.wasSuccessful():
    print '--++' * 20
    print 'Yeee you know what, all tests came out clean.'
    print '--++' * 20

  else:
    errors = len(my_results.errors)
    failures = len(my_results.failures)

    print my_results.printErrors()
    print FormatHeader('Tests failed.')
    print '  {0:>10s}: {1:d}\n  {2:>10s}: {3:d}\n  {4:>10s}: {5:d}'.format(
        'Errors', errors, 'Failures', failures, 'Total', errors + failures)
    print '+=' * 40


if __name__ == '__main__':
  # Modify the system path to first search the CWD.
  sys.path.insert(0, '.')

  test_results = RunTests([
      os.path.join('.', 'artifacts'), os.path.join('.', 'tools')])

  PrintResults(test_results)
  if not test_results.wasSuccessful():
    sys.exit(1)
