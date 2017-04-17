"""Generic (non-sgfmill-specific) test framework code."""

import sys
import unittest

# This makes TestResult ignore lines from this module in tracebacks
__unittest = True

class SupporterError(Exception):
    """Exception raised by support objects when something goes wrong.

    This is raised to indicate things like sequencing errors detected by mock
    objects.

    """

class SimpleTestCase(unittest.TestCase):
    """TestCase which runs a single function.

    Instantiate with the test function, which takes a TestCase parameter, eg:
        def test_xxx(tc):
            tc.assertEqual(2+2, 4)

    """

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        try:
            self.name = fn.__module__.split(".", 1)[-1] + "." + fn.__name__
        except AttributeError:
            self.name = str(fn)

    def runTest(self):
        self.fn(self)

    def id(self):
        return self.name

    def shortDescription(self):
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<SimpleTestCase: %s>" % self.name


class ParameterisedTestCase(unittest.TestCase):
    """Parameterised testcase.

    Subclasses should define:
      test_name       -- short string
      parameter_names -- list of identifiers
      runTest

    """
    def __init__(self, code, *parameters):
        super().__init__()
        self.code = code
        self.name = "%s.%s:%s" % (self.__class__.__module__.split(".", 1)[-1],
                                  self.test_name, code)
        for name, value in zip(self.parameter_names, parameters):
            setattr(self, name, value)

    def runTest(self):
        raise NotImplementedError

    def id(self):
        return self.name

    def shortDescription(self):
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)



def _function_sort_key(fn):
    try:
        return fn.__code__.co_firstlineno
    except AttributeError:
        return str(fn)

def make_simple_tests(source, prefix="test_", testcase_class=SimpleTestCase):
    """Make test cases from a module's test_xxx functions.

      source         -- dict (usually a module's globals()).
      prefix         -- string (default "test_")
      testcase_class -- SimpleTestCase subclass to use

    Returns a list of TestCase objects.

    This makes a TestCase for each function in the values of 'source' whose
    name begins with 'prefix'.

    The list is in the order of function definition (using the line number
    attribute).

    """
    functions = [value for name, value in source.items()
                 if name.startswith(prefix) and callable(value)]
    functions.sort(key=_function_sort_key)
    return [testcase_class(fn) for fn in functions]

