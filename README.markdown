# Introduction

validatron is a simple library for validating the structure and form of data.

# Where to use it

validatron is not meant to populate your system with self checks of constraints
at every layer, or at the interface between all internal components. This would
seem counter to the culture that goes with Python.

Rather, this library intends to provide a simple way to validate data coming in
from external systems. It is in these cases that it becomes beneficial to
check the entire structure of what was recieved, and fail fast if needed.

Further, this library does not replace the validation that is provided with
libraries and frameworks, like Django model validation.

Given all the above, this library will like be used somewhat rarely in your
system, only at the interfaces to external systems that you recieve data
from.

# Roadmap

This library currently exists as a sort of incubator in which to try three
specific styles of what validation might look like. The simplest and most
robust style should win out.

# Status

The "models" variation is pretty well fleshed out. The other two need some
more love before they can get a fair comparison.

## Models

This variation is largely inspired by Django models. You declare classes and
list field definitions to describe the expected structure.

## Contexts

This variation would provide a context manager that, when initialized with
the object or data to be validated, provides utility methods to express
the expecations against it.

## Expressions

This variation would expect validation to be expressed to look like the
expected structures. E.g., a dictionary of attribute names to fields
would describe an object or dictionary that should have attributes
fulfilling those field definitions.

# License

Licensed under the MIT license. See LICENSE.
