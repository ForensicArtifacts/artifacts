#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Tests for the artifact definitions validator."""

import glob
import os
import unittest

from artifacts import errors
from tools import validator

from tests import test_lib


class ArtifactDefinitionsValidatorTest(test_lib.BaseTestCase):
  """Class to test the validator."""

  def testArtifactDefinitionsValidator(self):
    """Runs the validator over all the YAML artifact definitions files."""
    validator_object = validator.ArtifactDefinitionsValidator()

    for definitions_file in glob.glob(os.path.join('data', '*.yaml')):
      result = validator_object.CheckFile(definitions_file)
      self.assertTrue(
          result, msg='in definitions file: {0}'.format(definitions_file))

    undefined_artifacts = validator_object.GetUndefinedArtifacts()
    if undefined_artifacts:
      raise errors.MissingDependencyError(
          'Artifacts group referencing undefined artifacts: {0}'.format(
              undefined_artifacts))

  # TODO: add tests that deliberately provide invalid definitions to see
  # if the validator works correctly.


if __name__ == '__main__':
  unittest.main()
