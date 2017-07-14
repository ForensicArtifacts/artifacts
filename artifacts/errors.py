# -*- coding: utf-8 -*-
"""The error objects."""


class Error(Exception):
  """The error interface."""


class CodeStyleError(Error):
  """Error that is raised when code formatting fails style checks."""


class FormatError(Error):
  """Error that is raised when the format is incorrect."""


class MissingDependencyError(Error):
  """Artifact references artifact that is undefined."""
