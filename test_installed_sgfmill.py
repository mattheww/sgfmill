"""Run the sgfmill testsuite against an installed sgfmill package."""

import imp
import os
import sys

from pathlib import Path

project_dir = Path(Path.cwd(), __file__).parent

# Remove the distribution directory from sys.path
if os.path.abspath(sys.path[0]) == str(project_dir):
    del sys.path[0]

try:
    import sgfmill
except ImportError:
    sys.exit("test_installed_sgfmill: can't find the sgfmill package")

PACKAGE_NAME = "sgfmill_tests"

# Make sgfmill_tests importable without the sibling sgfmill
packagepath = Path(project_dir, PACKAGE_NAME)
mdl = imp.load_package(PACKAGE_NAME, str(packagepath))
sys.modules[PACKAGE_NAME] = mdl

found = Path(Path.cwd(), sgfmill.__file__).parent
print("testing sgfmill package in %s" % found, file=sys.stderr)
from sgfmill_tests import run_sgfmill_testsuite
run_sgfmill_testsuite.run(sys.argv[1:])

