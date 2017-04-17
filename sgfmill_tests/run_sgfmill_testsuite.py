"""Construct and run the sgfmill testsuite."""

import unittest
import sys
from collections import defaultdict
from optparse import OptionParser

test_modules = [
    'common_tests',
    'board_tests',
    'sgf_grammar_tests',
    'sgf_properties_tests',
    'sgf_tests',
    'sgf_moves_tests',
    ]

def get_test_module(name):
    """Import the specified sgfmill_tests module and return it."""
    dotted_name = "sgfmill_tests." + name
    __import__(dotted_name)
    return sys.modules[dotted_name]

def run_testsuite(suite, failfast, buffer):
    """Run the specified testsuite.

    suite    -- TestSuite
    failfast -- bool (stop at first failing test)
    buffer   -- bool (show stderr/stdout only for failing tests)

    Output is to stderr

    """
    try:
        # This gives 'catchbreak' behaviour
        unittest.signals.installHandler()
    except Exception:
        pass
    runner = unittest.TextTestRunner(failfast=failfast, buffer=buffer)
    runner.run(suite)

class UnknownTest(Exception):
    """Unknown test module or test name."""

def make_testsuite(module_names, tests_by_module):
    """Import testsuite modules and make the TestCases.

    module_names    -- set of module names (empty means all)
    tests_by_module -- map module_name -> set of test names (empty means all)

    Returns a TestSuite.

    Test names are as given by test.id()
    For function-based tests, that means <module_name>.<function_name>
    For parameterised tests, it's <module_name>.<test_name>:<code>

    The tests in the returned suite are always in their 'natural' order; the
    order of command line items has no effect.

    Raises UnknownTest if a specified test or test module doesn't exist.

    """
    result = unittest.TestSuite()
    for module_name in sorted(module_names):
        if module_name not in test_modules:
            raise UnknownTest("unknown module: %s" % module_name)
    for module_name in test_modules:
        if module_names and (module_name not in module_names):
            continue
        mdl = get_test_module(module_name)
        suite = unittest.TestSuite()
        mdl.make_tests(suite)
        test_names = tests_by_module[module_name]
        if not test_names:
            result.addTests(suite)
            continue
        existing = set(test.id() for test in suite)
        for test_name in sorted(test_names):
            if test_name not in existing:
                raise UnknownTest("unknown test: %s" % test_name)
        for test in suite:
            if test.id() in test_names:
                result.addTest(test)
    return result

def interpret_args(args):
    """Interpret command-line arguments.

    Returns a pair (module_names, tests_by_module), for make_testsuite().

    """
    tests_by_module = defaultdict(set)
    module_names = set()
    for arg in args:
        module_name, is_compound, _ = arg.partition(".")
        module_names.add(module_name)
        if is_compound:
            tests_by_module[module_name].add(arg)
    return module_names, tests_by_module

def run(argv):
    parser = OptionParser(usage="%prog [options] [module|module.test] ...")
    parser.add_option("-f", "--failfast", action="store_true",
                      help="stop after first test")
    parser.add_option("-p", "--nobuffer", action="store_true",
                      help="show stderr/stdout for successful tests")
    (options, args) = parser.parse_args(argv)
    module_names, tests_by_module = interpret_args(args)
    try:
        suite = make_testsuite(module_names, tests_by_module)
    except UnknownTest as e:
        parser.error(str(e))
    run_testsuite(suite, options.failfast, not options.nobuffer)

if __name__ == "__main__":
    run(sys.argv[1:])

