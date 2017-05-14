#!/bin/bash
#
# Script to set up Travis-CI test VM.

COVERALL_DEPENDENCIES="python-coverage python-coveralls python-docopt";

L2TBINARIES_DEPENDENCIES="PyYAML";

L2TBINARIES_TEST_DEPENDENCIES="yapf";

PYTHON2_DEPENDENCIES="python-yaml";

PYTHON2_TEST_DEPENDENCIES="yapf";

PYTHON3_DEPENDENCIES="python3-yaml";

PYTHON3_TEST_DEPENDENCIES="python3-yapf";

# Exit on error.
set -e;

if test `uname -s` = "Darwin";
then
	git clone https://github.com/log2timeline/l2tdevtools.git;

	mv l2tdevtools ../;
	mkdir dependencies;

	PYTHONPATH=../l2tdevtools ../l2tdevtools/tools/update.py --download-directory=dependencies ${L2TBINARIES_DEPENDENCIES} ${L2TBINARIES_TEST_DEPENDENCIES};

elif test `uname -s` = "Linux";
then
	sudo add-apt-repository ppa:gift/dev -y;
	sudo apt-get update -q;
	sudo apt-get install -y ${COVERALL_DEPENDENCIES} ${PYTHON2_DEPENDENCIES} ${PYTHON2_TEST_DEPENDENCIES} ${PYTHON3_DEPENDENCIES} ${PYTHON3_TEST_DEPENDENCIES};
fi
