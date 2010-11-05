# coding=utf-8

__author__ = 'Steven Cummings'
__all__ = ('Field', 'StringField', 'NumberField', 'BooleanField')


from gettext import gettext as _

import decimal
import re


class Field(object):
    """
    Base class for model fields. It specifies whether or not a field is
    optional and a default value.

    Field itself cannot be instantiated, as its exclusive intended use is to
    derive concrete field types.

    >>> Field()
    Traceback (most recent call last):
        ...
    TypeError: Field should not be directly instantiated
    >>> f = StringField(optional=True, default_value='aString')
    >>> f.optional
    True
    >>> f.default_value
    'aString'
    >>> f.validate(None)
    """

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
            return _('missing')


class StringField(Field):
    """
    Field containing characters string (str and unicode) values.

    >>> import re
    >>> f = StringField(pattern=r'abc123', pattern_flags=re.IGNORECASE)
    >>> f.validate('abc123')
    >>> f.validate(u'ABC123')
    >>> f.validate(None)
    'missing'
    >>> f.validate('')
    'empty value'
    >>> f.validate(True)
    'not a string'
    >>> f.validate('xyz789')
    'non match'
    """ 

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
                return _('not a string')
            if len(value) == 0:
                return _('empty value')
            if self.pattern and not self.pattern.match(value):
                return _('non match')


class NumberField(Field):
    """
    Field containing numeric values.

    >>> f = NumberField(1, 50)
    >>> f.min_value
    1
    >>> f.max_value
    50
    >>> f.validate(None)
    'missing'
    >>> f.validate(0)
    'less than minimum'
    >>> f.validate(51)
    'greater than maximum'
    >>> f.validate('1')
    'not a number'
    >>> f.validate(3.14)
    >>> from decimal import Decimal
    >>> f.validate(Decimal('3.14'))
    """

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(NumberField, self).__init__(*args, **kwargs)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    def validate(self, value):
        base_problems = super(NumberField, self).validate(value)
        if base_problems:
            return base_problems
        if value is not None:
            if not isinstance(value, (int, long, float, decimal.Decimal)):
                return _('not a number')
            if self.min_value and value < self.min_value:
                return _('less than minimum')
            if self.max_value and value > self.max_value:
                return _('greater than maximum')


class BooleanField(Field):
    """
    Field containing only boolean (true or false) values.

    >>> f = BooleanField()
    >>> f.validate(None)
    'missing'
    >>> f.validate('aString')
    'not a boolean value'
    >>> f.validate(1)
    'not a boolean value'
    >>> f.validate(True)
    >>> f.validate(False)
    """

    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)

    def validate(self, value):
        base_problems = super(BooleanField, self).validate(value)
        if base_problems:
            return base_problems
        if value is not None:
            if not isinstance(value, bool):
                return _('not a boolean value')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
