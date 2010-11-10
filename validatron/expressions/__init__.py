# coding=utf-8

__all__ = ('validate', 'string', 'number', 'boolean')


from gettext import gettext as _

import decimal
import re


def validate(value, validator):
    """
    Validate the given value with the specified validator. If there are 
    validation problems, either a string message or dictionary of strings is
    returned. The dictionary is keyed by index if a list or tuple is being
    validated, or attribute name if a dictionary is being validated. If there
    are no problems, None is returned.

    >>> v1 = {"a": string(optional=True), "b": string(), "c": number()}
    >>> validate({"a": "aString", "b": "anotherString", "c": 1}, v1)
    >>> validate({"b": "anotherString", "c": 1}, v1)
    >>> validate({"c": 1}, v1)
    {'b': 'missing'}
    >>> validate({"b": "anotherString"}, v1)
    {'c': 'missing'}
    >>> validate({"b": "anotherString", "c": "notANumber"}, v1)
    {'c': 'not a number'}
    >>> v2 = [boolean()]
    >>> validate([True, True, False], v2)
    >>> validate([True, "True", False], v2)
    {1: 'not a boolean value'}
    >>> v3 = (string(), number())
    >>> validate(("a", 1), v3)
    >>> validate(("a", 1.0), v3)
    >>> validate(("a", "notANumber"), v3)
    {1: 'not a number'}
    >>> validate(("a",), v3)
    'unexpected tuple length: expected 2, got 1'
    >>> validate("a", string())

    """

    if isinstance(validator, dict):
        return _validate_dict(value, validator)
    elif isinstance(validator, list):
        return _validate_list(value, validator)
    elif isinstance(validator, tuple):
        return _validate_tuple(value, validator)
    elif callable(validator):
        return validator(value)
    else:
        raise TypeError('Unexpected type for validator: {0}'.format(
                        type(validator)))


def _validate_dict(value, validator):
    if not isinstance(value, dict):
        return _('not a dict')
    problems = {}
    for attr_name, attr_validator in validator.iteritems():
        attr_value = value[attr_name] if attr_name in value else None
        result = attr_validator(attr_value)
        if result:
            problems[attr_name] = result
    return problems or None


def _validate_list(value, validator):
    if not isinstance(value, list):
        return _('not a list')
    if len(validator) != 1:
        return _('should have only one element validator for list')
    problems = {}
    element_validator = validator[0]
    for index, element in enumerate(value):
        result = element_validator(element)
        if result:
            problems[index] = result
    return problems or None


def _validate_tuple(value, validator):
    if not isinstance(value, tuple):
        return _('not a tuple')
    if len(value) != len(validator):
        return _('unexpected tuple length: expected {0}, got {1}').format(
                 len(validator), len(value))
    problems = {}
    for index, (element, element_validator) in enumerate(zip(value, validator)):
        result = element_validator(element)
        if result:
            problems[index] = result
    return problems or None


def string(optional=False, empty=False, pattern=None, pattern_flags=None):
    """
    Returns a function that validates a value as a string based on the 
    specified criteria.

    >>> v1 = string()
    >>> v1('aString')
    >>> v1(None)
    'missing'
    >>> v1('')
    'empty value'
    >>> v2 = string(optional=True, empty=True, pattern=r'^\d+$')
    >>> v2(None)
    >>> v2('')
    >>> v2('1234')
    >>> v2('a')
    'non match'

    """

    rx = (re.compile(pattern, pattern_flags) 
          if pattern_flags 
          else re.compile(pattern)
          if pattern else None)
    def is_valid(value):
        if value is not None:
            if not isinstance(value, basestring):
                return _('not a string')
            if not empty and len(value) == 0:
                return _('empty value')
            if value and rx and not rx.match(value):
                return _('non match')
        else:
            if not optional:
                return _("missing")
    return is_valid


def number(optional=False, min_value=None, max_value=None):
    """
    Returns a function that validates a value as a number based on the
    specified criteria.

    >>> v1 = number(min_value=0, max_value=10)
    >>> v1(1)
    >>> v1(1.0)
    >>> v1(decimal.Decimal('1.0'))
    >>> v1(None)
    'missing'
    >>> v1('aString')
    'not a number'
    >>> v1(-1)
    'less than minimum'
    >>> v1(11)
    'greater than maximum'

    """

    def is_valid(value):
        if value is not None:
            if not isinstance(value, (int, long, float, decimal.Decimal)):
                return _('not a number')
            if min_value is not None and value < min_value:
                return _('less than minimum')
            if max_value is not None and value > max_value:
                return _('greater than maximum')
        else:
            if not optional:
                return _("missing")
    return is_valid


def boolean(optional=False):
    """
    Returns a function that validates a value as a boolean based on the
    specified criteria.

    >>> v1 = boolean()
    >>> v1(True)
    >>> v1(False)
    >>> v1(None)
    'missing'
    >>> v1('aString')
    'not a boolean value'

    """

    def is_valid(value):
        if value is not None:
            if not isinstance(value, bool):
                return _('not a boolean value')
        else:
            if not optional:
                return _("missing")
    return is_valid


if __name__ == '__main__':
    import doctest
    doctest.testmod()
