
import re

import yaml

class IncorrectTypeError(Exception):
    message = 'The value does not match the type in the specification'


class IncorrectLengthError(Exception):
    message = 'The value does not meet the length requirements'


class IncorrectPatternError(Exception):
    message = 'The value does not conform to the correct pattern'


class IncorrectSpecificationError(Exception):
    message = 'There is an issue with your configuration specification'


class SafeYaml(dict):

    def __init__(self, filename, specification):
        self.spec = specification
        with open(filename, 'r') as f:
            config = yaml.load(f)
        for k,v in config.iteritems():
            self.check_type(k, v)
            self.check_length(k, v)
            self.check_pattern(k, v)
            self.__setitem__(str(k), v)

    def check_type(self, key, val):
        # TODO: add types: path, url, hostname, json
        _type = self.spec[key]['type']
        if isinstance(val, _type):
            return
        else:
            raise IncorrectTypeError

    def check_length(self, key, val):
        try:
            _min = self.spec[key]['length']['min']
            _max = self.spec[key]['length']['max']
        except KeyError:
            return
        if _min > _max:
            raise IncorrectSpecificationError
        length = len(val)
        if length < _min or length > _max:
            raise IncorrectLengthError
        else:
            return

    def check_pattern(self, key, val):
        try:
            pattern = self.spec[key]['pattern']
        except Exception:
            return
        if pattern.match(val):
            return
        else:
            raise IncorrectPatternError
