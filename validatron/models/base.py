# coding=utf-8


"""
>>> class Person(Model):
...     first_name = StringField()
...     last_name = StringField()
...     middle_name = StringField(optional=True)
...     age = NumberField()
>>> Person().validate()
{'age': 'missing', 'last_name': 'missing', 'first_name': 'missing'}
>>> Person(first_name='John', last_name='Smith', age=20).validate()
>>> class Address(Model):
...     street = StringField()
...     city = StringField()
...     region = StringField()
...     country = StringField(optional=True)
...     postal_code = StringField(pattern=r'^\d{5}$')
...     is_business = BooleanField()
>>> Address().validate()
{'city': 'missing', 'is_business': 'missing', 'street': 'missing', 'postal_code': 'missing', 'region': 'missing'}
>>> a = Address(street='101 4th',city='Townville',region='Missouri',
...             country='US',postal_code='64000',is_business=False)
>>> a.validate()
>>> a.postal_code = 'bad'
>>> a.validate()
{'postal_code': 'non match'}
>>> # Let's try some inheritance now
>>> class Root(Model):
...     a = StringField()
>>> class ParentA(Root):
...     b = NumberField()
>>> class ParentB(Model):
...     c = StringField()
>>> class Derived(ParentA, ParentB):
...     b = NumberField(optional=True)
...     c = BooleanField()
>>> Derived().validate()
{'a': 'missing', 'c': 'missing'}
>>> Derived(a='aString',c=True).validate()
"""


__author__ = 'Steven Cummings'
__all__ = ('Model',)


from fields import Field, StringField, NumberField, BooleanField


class ValidationModelMetadata(object):
    """
    Holds field information extracted from a class definition that specifies
    ModelType as its metaclass.
    """

    def __init__(self):
        self._fields = {}

    @property
    def fields(self):
        return self._fields

    def inherit_from(self, other):
        for field_name, field in other.fields.iteritems():
            if field_name not in self.fields:
                self.fields[field_name] = field


class ModelType(type):
    """
    Metaclass for validation models. Extracts the field definitions and stores
    them as a new attribute of the class, _meta, which has type 
    ValidationModelMetadata.
    """

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
    """
    Base class for validation models. Provides a method, validate, which
    tests the values of a model instance against the declared fields and
    their validation constraints.
    """

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
