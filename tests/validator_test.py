#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the artifact definitions validator."""

import glob
import os
import unittest

from artifacts import errors
from artifacts.scripts import validator

from tests import test_lib


class ArtifactDefinitionsValidatorTest(test_lib.BaseTestCase):
  """Class to test the validator."""

  def testArtifactDefinitionsValidator(self):
    """Runs the validator over all the YAML artifact definitions files."""
    validator_object = validator.ArtifactDefinitionsValidator()

    data_files_glob = os.path.join(self._DATA_PATH, '*.yaml')
    for definitions_file in glob.glob(data_files_glob):
      result = validator_object.CheckFile(definitions_file)
      self.assertTrue(
          result, msg=f'in definitions file: {definitions_file:s}')

    undefined_artifacts = validator_object.GetUndefinedArtifacts()
    if undefined_artifacts:
      undefined_artifacts = ', '.join(undefined_artifacts)
      raise errors.MissingDependencyError((
          f'Artifacts group referencing undefined artifacts: '
          f'{undefined_artifacts:s}'))

  # TODO: add tests that deliberately provide invalid definitions to see
  # if the validator works correctly.


if __name__ == '__main__':
  unittest.main()
