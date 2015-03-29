# -*- coding: utf-8 -*-
"""The error objects."""


class Error(Exception):
  """The error interface."""


class FormatError(Error):
  """Error that is raised when the format is incorrect."""
