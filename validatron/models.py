# TODO create an i18n/l10n-able message registry

"""
>>> class C(Model):
...     a = Field()
...     b = Field(optional=True)
...     c = StringField()
>>> c0 = C()
>>> c0.validate()
{'a': 'missing', 'c': 'missing'}
>>> c1 = C(a=1,c='aString')
>>> c1.validate()
>>> c2 = C(c='aString')
>>> c2.validate()
{'a': 'missing'}
>>> c3 = C(a=1)
>>> c3.validate()
{'c': 'missing'}
>>> c4 = C(a=1, c='')
>>> c4.validate()
{'c': 'missing'}
"""


class Field(object):
    def __init__(self, optional=False, default_value=None):
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
    # TODO pattern option
    def validate(self, value):
        base_problems = super(StringField, self).validate(value)
        if base_problems:
            return base_problems
        if len(value) == 0:
            return 'missing'


class ValidationModelMetadata(object):
    def __init__(self):
        self.fields = {}
    def inherit_from(self, other):
        for field_name, attr in other.fields.iteritems():
            if field_name not in self.fields:
                self.fields[field_name] = field


class ModelType(type):
    def __new__(cls, name, bases, attrs):
        _meta = ValidationModelMetadata()
        for attr_name, attr in attrs.iteritems():
            if isinstance(attr, Field):
                _meta.fields[attr_name] = attr
        for attr_name in _meta.fields.keys():
            del attrs[attr_name]

        new_class = super(ModelType, cls).__new__(cls, name, bases, attrs)

        def is_inheritable(parent):
            return isinstance(parent, ModelType) and hasattr(parent, '_meta')

        for parent in new_class.__mro__:
            if (not parent is cls and is_inheritable(parent)):
                _meta.inherit_from(parent._meta)
        setattr(new_class, '_meta', _meta)

        return new_class


class Model(object):
    __metaclass__ = ModelType
    def __init__(self, **kwargs):
        for field_name, field in self._meta.fields.iteritems():
            setattr(self, field_name, field.default_value)
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    def validate(self):
        """
        Validates the current instance against the declared fields of the 
        class. Return a dictionary of validation problems keyed by offended
        field, if there are any, otherwise None.

        A field's validation problems can be one of:
        -   An individual problem string
        -   A list of problem strings
        -   Dictionary of problems for the attributes or elements of the field. 
        """
        problems = {}
        for field_name, field in self._meta.fields.iteritems():
            value = getattr(self, field_name, None)
            field_problems = field.validate(value)
            if field_problems:
                problems[field_name] = field_problems
        return problems or None



if __name__ == '__main__':
    import doctest
    doctest.testmod()
