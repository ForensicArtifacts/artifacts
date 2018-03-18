#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to check for the availability and version of dependencies."""

import sys

# Change PYTHONPATH to include dependencies.
sys.path.insert(0, '.')

import utils.dependencies  # pylint: disable=wrong-import-position


if __name__ == '__main__':
  dependency_helper = utils.dependencies.DependencyHelper()

  dependency_helper.CheckDependencies()
