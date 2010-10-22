# coding=utf-8

"""
>>> from fields import StringField, IntegerField
>>> class C(Model):
...     a = IntegerField()
...     b = StringField(optional=True)
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

from fields import *
from base import *


if __name__ == '__main__':
    import doctest
    doctest.testmod()
