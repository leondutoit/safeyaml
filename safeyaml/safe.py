
import os
import re

import yaml

from url import IS_VALID_URL


class IncorrectTypeError(Exception):
    pass


class IncorrectLengthError(Exception):
    pass


class IncorrectPatternError(Exception):
    pass


class IncorrectSpecificationError(Exception):
    message = 'There is an issue with your configuration specification'


class InvalidPathError(Exception):
    pass


class InvalidUrlError(Exception):
    pass


class InvalidHostNameError(Exception):
    pass


class MissingKeyError(Exception):
    message = 'Your config specification is missing a key'


class SafeYaml(dict):

    """Safely construct a dictionary from a YAML file."""

    def __init__(self, filename, specification):
        self.spec = specification
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        self.check_keys(config, specification)
        for k,v in config.iteritems():
            self.check_type(k, v)
            self.check_length(k, v)
            self.check_pattern(k, v)
            self.__setitem__(str(k), v)

    def check_keys(self, config, spec):
        config_keys = config.keys()
        spec_keys = spec.keys()
        for k in config_keys:
            if k in spec_keys:
                pass
            else:
                raise MissingKeyError
        return

    def check_type(self, key, val):
        _type = self.spec[key]['type']
        if issubclass(_type, CustomType):
            # validate by checking if we can construct it
            obj = _type(val)
            return
        if isinstance(val, _type):
            return
        else:
            message = 'Value: %s, for key: %s, does not match type in spec: %s' % (str(val), str(key), str(_type))
            raise IncorrectTypeError(message)

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
            message = 'Value for key: %s, has length %d, requirements are - min: %d, max: %d' % (key, length, _min, _max)
            raise IncorrectLengthError(message)
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
            message = 'The value: %s, does not conform to the correct pattern' % val
            raise IncorrectPatternError(message)


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
            message = 'The path %s does not exist' % name
            raise InvalidPathError(message)


class Url(CustomType):

    """Valid URL?"""

    def __init__(self, name):
        self.name = self.check_url(name)

    def check_url(self, name):
        if IS_VALID_URL.match(name):
            return name
        else:
            message = 'Invalid URL: %s' % name
            raise InvalidUrlError(message)


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
            message = 'Invalid host name: %s' % name
            raise InvalidHostNameError(message)
