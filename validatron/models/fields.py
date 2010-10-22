# coding=utf-8

# TODO create an i18n/l10n-able message registry

"""
"""


__author__ = 'Steven Cummings'
__all__ = ('Field', 'StringField', 'IntegerField')


import re


class Field(object):
    def __init__(self, optional=False, default_value=None):
        if type(self) is Field:
            raise TypeError('Field should not be directly instantiated')
        self._optional = optional
        self._default_value = default_value
    @property
    def optional(self):
        return self._optional
    @property
    def default_value(self):
        return self._default_value
    def validate(self, value):
        if not self.optional and value is None:
            return 'missing'


class StringField(Field):
    def __init__(self, pattern=None, pattern_flags=None, *args, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self._pattern = (re.compile(pattern, pattern_flags) 
                         if pattern_flags 
                         else re.compile(pattern)
                         if pattern else None)

    @property
    def pattern(self):
        return self._pattern

    def validate(self, value):
        base_problems = super(StringField, self).validate(value)
        if base_problems:
            return base_problems
        if value is not None:
            if not isinstance(value, basestring):
                return 'not a string'
            if len(value) == 0:
                return 'missing'
            if self.pattern and not self.pattern.match(value):
                return 'non match'


class IntegerField(Field):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    def validate(self, value):
        base_problems = super(IntegerField, self).validate(value)
        if base_problems:
            return base_problems
        if value is not None:
            if not isinstance(value, (int, long)):
                return 'not an integer'
            if self.min_value and value < self.min_value:
                return 'less than minimum'
            if self.max_value and value > self.max_value:
                return 'greater than maximum'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
