__all__ = ('ValidationError', 'string', 'floating_point', 'integer', 'decimal', 'boolean')


from decimal import Decimal


class ValidationError(ValueError):
    def __init__(self, problems):
        self.problems = problems


# TODO datetime


def string(optional=False, min_length=1, max_length=None, pattern=None):
    def is_valid(value):
        if value is not None:
            if not isinstance(value, basestring):
                return "not a string"
            if min_length is not None and len(value) < min_length:
                return "too short"
            if max_length is not None and len(value) > max_length:
                return "too long"
            # TODO pattern
            return None
        else:
            if not optional:
                return "missing"
    return is_valid


def integer(optional=False, min_value=None, max_value=None):
    def is_valid(value):
        if value is not None:
            if not isinstance(value, (int, long)):
                return "not a whole number"
            if min_value is not None and value < min_value:
                return "too small"
            if max_value is not None and value > max_value:
                return "too large"
            return None
        else:
            if not optional:
                return "missing"
    return is_valid


def floating_point(optional=False, min_value=None, max_value=None):
    def is_valid(value):
        if value is not None:
            if not isinstance(value, float):
                return "not a floating-point number"
            if min_value is not None and value < min_value:
                return "too small"
            if max_value is not None and value > max_value:
                return "too large"
            return None
        else:
            if not optional:
                return "missing"
    return is_valid


def decimal(optional=False, min_value=None, max_value=None):
    def is_valid(value):
        if value is not None:
            if not isinstance(value, Decimal):
                return "not a decimal number"
            if min_value is not None and value < min_value:
                return "too small"
            if max_value is not None and value > max_value:
                return "too large"
            return None
        else:
            if not optional:
                return "missing"
    return is_valid


def boolean(optional=False):
    def is_valid(value):
        if value is not None:
            if not isinstance(value, bool):
                return "not a boolean"
            return None
        else:
            if not optional:
                return "missing"
    return is_valid
