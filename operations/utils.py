from logging import getLogger
from functools import reduce
from operator import add, sub, mul, truediv

# Core operations for calculator

def calculate(operation_type, values):
    """Return the result of accumulation of values for an operation type
    >>> calculate('sum', [10.0, 20.0, 30.0])
    60.0
    >>> calculate('sub', [10.0, 20.0, 30.0])
    -40.0
    Some arithmetic constraints should be noted, such as zero division:
    >>> calculate('sub', [10.0, 0.0])
    Traceback (most recent call last):
    ZeroDivisionError: division by zero
    """
    log = getLogger()
    operators = { 
        'sum': add, 
        'sub': sub, 
        'mul': mul, 
        'div': truediv 
    } # Operators dictionary for selecting operator
    try: 
        log.info("Operating values {} with {}" . format(values, operation_type))
        result = reduce(operators[operation_type], values)
    except ZeroDivisionError:
        log.error("Error while dividing by zero")
        result = 0.0
    return result # Returns value of reducing an array of values by type operation_type