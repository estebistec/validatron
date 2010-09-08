def validate(value, validator):
    """
    >>> from core import string, integer
    >>> v = {"a": string(optional=True), "b": string()}
    >>> validate({"a": "aString", "b": "anotherString"}, v)
    >>> validate({"b": "anotherString"}, v)
    >>> validate({}, v)
    {'b': 'missing'}
    """
    if isinstance(validator, dict):
        if not isinstance(value, dict):
            return {'__all__': 'Wrong type. Expected dict, got {type}'.format(type=type(value))}
        return _validate_dict(value, validator)
    elif isinstance(validator, list):
        if not isinstance(validator, list):
            return {'__all__': 'Wrong type. Expected list, got {type}'.format(type=type(value))}
        return _validate_sequence(value, validator)
    # TODO tuple
    elif callable(validator):
        return validator(value)
    else:
        raise TypeError('Unexpected type for rules: {0}'.format(type(rules)))

def _validate_dict(value, validator):
    problems = {}
    for attr_name, attr_validator in validator.iteritems():
        attr_value = value[attr_name] if attr_name in value else None
        result = attr_validator(attr_value)
        if result:
            problems[attr_name] = result
    return problems or None

def _validate_sequence(value, validator):
    problems = {}
    element_validator = validator[0]
    for index, element in enumerate(value):
        result = element_validator(element)
        if result:
            problems[index] = result
    return problems or None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
