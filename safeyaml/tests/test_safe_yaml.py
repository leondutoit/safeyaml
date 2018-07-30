
import os
import re
import unittest

from ..safe import SafeYaml, IncorrectTypeError, IncorrectLengthError, \
                   IncorrectPatternError, IncorrectSpecificationError, \
                   Path, Url, HostName, InvalidPathError, InvalidUrlError, \
                   InvalidHostNameError


class TestSafeYaml(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.example_file = os.path.expanduser('~/safeyaml/safeyaml/tests/example.yaml')

    def test_can_construct_object_with_correct_spec(self):
        spec = {
            'one': {'type': str, 'length': {'min': 2, 'max': 3}, 'pattern': re.compile(r'[a-z]')},
            'two': {'type': int},
            'three': {'type': bool},
            'four': {'type': dict},
            'five': {'type': list},
            'six': {'type': Path},
            'seven': {'type': Url},
            'eight': {'type': HostName},
        }
        config = SafeYaml(self.example_file, spec)
        self.assertTrue(isinstance(config, SafeYaml))


def main():
    runner = unittest.TextTestRunner()
    suite = []
    suite.append(unittest.TestSuite(map(TestSafeYaml, [
                 'test_can_construct_object_with_correct_spec',])))
    map(runner.run, suite)


if __name__ == '__main__':
    main()
