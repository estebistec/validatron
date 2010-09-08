class ValidationError(ValueError):
    def __init__(self, problems):
        self.problems = problems

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
            if not isinstance(value, int, long):
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

# TODO float
# TODO datetime
