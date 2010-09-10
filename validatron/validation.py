__all__ = ('validate',)

def validate(value, validator):
    """
    >>> from core import string, integer,boolean
    >>>
    >>> v_dict = {"a": string(optional=True), "b": string(), "c": integer()}
    >>> validate({"a": "aString", "b": "anotherString", "c": 1}, v_dict)
    >>> validate({"b": "anotherString", "c": 1}, v_dict)
    >>> validate({"c": 1}, v_dict)
    {'b': 'missing'}
    >>> validate({"b": "anotherString"}, v_dict)
    {'c': 'missing'}
    >>> validate({"b": "anotherString", "c": "notAnInt"}, v_dict)
    {'c': 'not a whole number'}
    >>>
    >>> v_list = [boolean()]
    >>> validate([True, True, False], v_list)
    >>> validate([True, "True", False], v_list)
    {1: 'not a boolean'}
    >>>
    >>> v_tuple = (string(), integer())
    >>> validate(("a", 1), v_tuple)
    >>> validate(("a", 1.0), v_tuple)
    {1: 'not a whole number'}
    >>> validate(("a",), v_tuple)
    {'__all__': 'unexpected tuple length: expected 2, got 1'}
    """
    if isinstance(validator, dict):
        if not isinstance(value, dict):
            return {'__all__': 'Wrong type. Expected dict, got {type}'.format(type=type(value))}
        return _validate_dict(value, validator)
    elif isinstance(validator, list):
        if not isinstance(validator, list):
            return {'__all__': 'Wrong type. Expected list, got {type}'.format(type=type(value))}
        return _validate_list(value, validator)
    elif isinstance(validator, tuple):
        return _validate_tuple(value, validator)
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

def _validate_list(value, validator):
    problems = {}
    if len(validator) != 1:
        raise ValueError('got multiple element validators for list')
    element_validator = validator[0]
    for index, element in enumerate(value):
        result = element_validator(element)
        if result:
            problems[index] = result
    return problems or None

def _validate_tuple(value, validator):
    problems = {}
    if len(value) != len(validator):
        problems['__all__'] = 'unexpected tuple length: expected {0}, got {1}'.format(len(validator), len(value))
    for index, (element, element_validator) in enumerate(zip(value, validator)):
        result = element_validator(element)
        if result:
            problems[index] = result
    return problems or None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
