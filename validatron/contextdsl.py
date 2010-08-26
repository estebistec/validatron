# encoding: utf-8

"""
>>> class A(object):
...     def __init__(self, a, b):
...         self.a = a
...         self.b = b
...
>>> class B(object):
...     def __init__(self, b):
...         self.b = b
...
>>> b = B('teh b')
>>> a = A(1, b)
>>> d = {'a': 1, 'b': {'b': 'teh b'}}
>>> def validate_a(a):
...     with validate(a) as v:
...         v.require('a')
...         v.require('b')
...         with v.validate('b') as v_b:
...             v_b.require('b')
...
>>> validate_a(a)
>>> validate_a(d)
>>> validate_a({})
Traceback (most recent call last):
    ...
ValidationException: {'a': ['missing'], 'b': ['missing']}
>>> validate_a({'a': 1})
Traceback (most recent call last):
    ...
ValidationException: {'b': ['missing']}
>>> validate_a({'a': 1, 'b': None})
>>> validate_a({'a': 1, 'b': {}})
Traceback (most recent call last):
    ...
ValidationException: {'b': {'b': ['missing']}}
"""

__author__ = 'Steven Cummings'

import os
import pprint
import sys

from contextlib import contextmanager

class ValidationContext(object):
    def __init__(self, obj):
        self.obj = obj
        self.problems = {}
    def require(self, name):
        if not self._has_attr(name):
            self.add_problem(name, 'missing')
    def not_none(self, name):
        if not (self._has_attr(name) 
                and self._get_attr(name) is not None):
            self.add_problem(name, 'None')
    def positive(self, name):
        if not (self._has_attr(name) 
                and self._get_attr(name) > 0):
            self.add_problem(name, 'non-positive')
    def non_negative(self, name):
        if not (self._has_attr(name) 
                and self._get_attr(name) >= 0):
            self.add_problem(name, 'negative')
    def add_problem(self, name, problem):
        self.problems.setdefault(name, []).append(problem)
    @contextmanager
    def validate(self, name):
        if self._has_attr(name) and self._get_attr(name) is not None:
            v = ValidationContext(self._get_attr(name))
            yield v
            if v.problems:
                self.problems[name] = v.problems
        else:
            # There's got to be a way to cancel execution of the nested block
            # instead of this...
            yield NullValidationContext()
    # Not crazy about the type checking here
    def _has_attr(self, name):
        if isinstance(self.obj, dict):
            return self.obj.has_key(name)
        else:
            return hasattr(self.obj, name)
    def _get_attr(self, name):
        if isinstance(self.obj, dict):
            return self.obj[name]
        else:
            return getattr(self.obj, name)

class NullValidationContext(object):
    def __getattr__(self, name):
        def no_op(*args, **kwargs):
            pass
        return no_op

class ValidationException(ValueError):
    def __init__(self, problems):
        self.problems = problems
    def __str__(self):
        return str(self.problems)
        #return pprint.format(self.problems)

@contextmanager
def validate(obj):
    v = ValidationContext(obj)
    yield v
    if v.problems:
        raise ValidationException(v.problems)

if __name__ == '__main__':
	import doctest
	doctest.testmod()
