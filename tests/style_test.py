"""Enforce code style."""

import subprocess
import unittest

from artifacts import errors


class StyleTest(unittest.TestCase):
  """Enforce code style requirements."""

  def testCodeStyle(self):
    """Check yapf style enforcement runs cleanly."""
    try:
      subprocess.check_output(
          ['yapf', '--diff', '-r', 'artifacts tools', 'artifacts', 'tests'])
    except subprocess.CalledProcessError as e:
      if hasattr(e, 'output'):
        raise errors.CodeStyleError(
            'Run "yapf -i -r artifacts tools/ artifacts/ tests/" to correct '
            'these problems: {0}'.format(e.output))
      raise


if __name__ == '__main__':
  unittest.main()
