
import os
import re

import yaml

from url import IS_VALID_URL


class IncorrectTypeError(Exception):
    message = 'The value does not match the type in the specification'


class IncorrectLengthError(Exception):
    message = 'The value does not meet the length requirements'


class IncorrectPatternError(Exception):
    message = 'The value does not conform to the correct pattern'


class IncorrectSpecificationError(Exception):
    message = 'There is an issue with your configuration specification'


class InvalidPathError(Exception):
    message = 'The path does not exist'


class InvalidUrlError(Exception):
    message = 'Invalid URL'


class InvalidHostNameError(Exception):
    message = 'Invalid host name'


class SafeYaml(dict):

    """Safely construct a dictionary from a YAML file."""

    def __init__(self, filename, specification):
        self.spec = specification
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        for k,v in config.iteritems():
            self.check_type(k, v)
            self.check_length(k, v)
            self.check_pattern(k, v)
            self.__setitem__(str(k), v)

    def check_type(self, key, val):
        _type = self.spec[key]['type']
        if issubclass(_type, CustomType):
            # validate by checking if we can construct it
            obj = _type(val)
            return
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


class CustomType(object):
    pass


class Path(CustomType):

    """Checks whether the path refers to an existing location."""

    def __init__(self, name):
        self.name = self.check_valid_path(name)

    def check_valid_path(self, name):
        if os.path.lexists(name):
            return name
        else:
            raise InvalidPathError


class Url(CustomType):

    """Valid URL?"""

    def __init__(self, name):
        self.name = self.check_url(name)

    def check_url(self, name):
        if IS_VALID_URL.match(name):
            return name
        else:
            raise InvalidUrlError


class HostName(CustomType):

    """Valid hostname?"""

    def __init__(self, name):
        self.name = self.check_host_name(name)

    def is_valid_hostname(self, hostname):
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        if len(hostname) > 253:
            return False
        labels = hostname.split(".")
        # the TLD must be not all-numeric
        if re.match(r"[0-9]+$", labels[-1]):
            return False
        allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(label) for label in labels)

    def check_host_name(self, name):
        if self.is_valid_hostname(name):
            return name
        else:
            raise InvalidHostNameError
