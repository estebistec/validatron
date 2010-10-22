# coding=utf-8

# TODO create an i18n/l10n-able message registry



__author__ = 'Steven Cummings'
__all__ = ('Model',)


from fields import Field


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
