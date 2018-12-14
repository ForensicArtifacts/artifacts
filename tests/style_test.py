"""Enforce code style."""

import subprocess
import unittest

from artifacts import errors

from tests import test_lib


class StyleTest(test_lib.BaseTestCase):
  """Enforce code style requirements."""

  @unittest.skip('yapf deployment need to be fixed')
  def testCodeStyle(self):
    """Check yapf style enforcement runs cleanly."""
    try:
      subprocess.check_output(
          ['yapf', '--diff', '-r', 'artifacts tools', 'artifacts', 'tests'])
    except subprocess.CalledProcessError as exception:
      if hasattr(exception, 'output'):
        raise errors.CodeStyleError(
            'Run "yapf -i -r artifacts tools/ artifacts/ tests/" to correct '
            'these problems: {0}'.format(exception.output))
      raise


if __name__ == '__main__':
  unittest.main()
