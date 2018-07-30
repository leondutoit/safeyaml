
## safeyaml

YAML is great, but it can also be an attack vector for you app. Even though using the `safe_load` function helps limit the attack surface, an attacker can still easily misconfigure something in a malignent way. In addition, it is easy for you to make a mistake in your own benign configuration.

`safeyaml` is designed to make it harder to perform config attacks based on python code execution, and to make it easier to catch accidental configuration mistakes.

It does so by forcing you to specify the type of each option, and gives you the ability to specify additional restrictions on specific types. If there is any deviation from the specification when config is loaded, then it will raise an exception.

## Usage

Suppose you had a YAML config file as such:

```yaml
one: val
two: 1
three: False
four:
  el1: val1
  el2: val2
five:
- l1
- l2
six: '/tmp'
seven: 'https://e.com'
eight: 'my-host.name.domain01
```

You can then use `safeyaml` to safely construct a config dictionary as such:

```python
from safeyaml import SafeYaml

config_specification = {
    'one': {'type': str, 'length': {'min': 2, 'max': 3},
            'pattern': re.compile(r'[a-z]')},
    'two': {'type': int},
    'three': {'type': bool},
    'four': {'type': dict},
    'five': {'type': list},
    'six': {'type': Path},
    'seven': {'type': Url},
    'eight': {'type': HostName},
}

config = SafeYaml('myfile.yaml', config_specification)

```

## LICENSE

BSD.
