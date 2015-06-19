#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the artifact definitions validator."""

import glob
import unittest
import os

from tools import validator


class ArtifactDefinitionsValidatorTest(unittest.TestCase):
  """Class to test the validator."""

  def testArtifactDefinitionsValidator(self):
    """Runs the validator over all the YAML artifact definitions files."""
    validator_object = validator.ArtifactDefinitionsValidator()
    for definitions_file in glob.glob(os.path.join('definitions', '*.yaml')):
      result = validator_object.CheckFile(definitions_file)
      self.assertTrue(result, msg='in definitions file: {0:s}'.format(
          definitions_file))

  # TODO: add tests that deliberately provide invalid definitions to see
  # if the validator works correctly.


if __name__ == '__main__':
  unittest.main()
