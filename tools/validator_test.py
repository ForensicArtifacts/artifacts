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
"""Tests for the artifact definitions validator."""

import glob
import unittest
import os

from tools import validator


class ValidatorTest(unittest.TestCase):
  """Class to test the validator."""

  def testRun(self):
    """Runs the validator over all the YAML artifact definition data files."""
    validator_object = validator.Validator()
    for data_file in glob.glob(os.path.join('data', '*.yaml')):
      result = validator_object.Run(data_file)
      self.assertTrue(result)


if __name__ == '__main__':
  unittest.main()
