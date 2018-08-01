
import os
import re
import unittest

from ..safe import SafeYaml, IncorrectTypeError, IncorrectLengthError, \
                   IncorrectPatternError, IncorrectSpecificationError, \
                   Path, Url, HostName, InvalidPathError, InvalidUrlError, \
                   InvalidHostNameError, MissingKeyError


class TestSafeYaml(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.example_file = os.path.expanduser('~/safeyaml/safeyaml/tests/example.yaml')
        cls.correct_spec = {
            'one': {'type': str, 'length': {'min': 1, 'max': 6}, 'pattern': re.compile(r'[a-z]')},
            'two': {'type': int},
            'three': {'type': bool},
            'four': {'type': dict},
            'five': {'type': list},
            'six': {'type': Path},
            'seven': {'type': Url},
            'eight': {'type': HostName},
        }

    def test_can_construct_object_with_correct_spec(self):
        config = SafeYaml(self.example_file, self.correct_spec)
        self.assertTrue(isinstance(config, SafeYaml))

    def test_cannot_construct_object_when_key_missing_from_spec(self):
        incorrect_spec = self.correct_spec
        incorrect_spec.pop('one')
        self.assertRaises(MissingKeyError, SafeYaml, self.example_file, incorrect_spec)

    def test_str_restrictions_work(self):
        incorrect_spec = self.correct_spec
        incorrect_spec['one'] = {'type': str, 'length': {'min': 4, 'max': 5}}
        self.assertRaises(IncorrectLengthError, SafeYaml, self.example_file, incorrect_spec)
        incorrect_spec['one'] = {'type': str, 'length': {'min': 600, 'max': 5}}
        self.assertRaises(IncorrectSpecificationError, SafeYaml, self.example_file, incorrect_spec)
        incorrect_spec['one'] = {'type': str, 'pattern': re.compile(r'[A-Z]')}
        self.assertRaises(IncorrectPatternError, SafeYaml, self.example_file, incorrect_spec)

    def test_path(self):
        self.assertRaises(InvalidPathError, Path, 'not-a-real-path')

    def test_url(self):
        self.assertRaises(InvalidUrlError, Url, 'h%tps:\\not-a-good?url^')

    def test_hostname(self):
        self.assertRaises(InvalidHostNameError, HostName, 'this*is%not+allowed.com')


def main():
    runner = unittest.TextTestRunner()
    suite = []
    suite.append(unittest.TestSuite(map(TestSafeYaml, [
                 'test_can_construct_object_with_correct_spec',
                 'test_cannot_construct_object_when_key_missing_from_spec',
                 'test_str_restrictions_work',
                 'test_path',
                 'test_url',
                 'test_hostname'])))
    map(runner.run, suite)


if __name__ == '__main__':
    main()
