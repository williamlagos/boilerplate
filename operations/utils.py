from functools import reduce
from operator import add, sub, mul, truediv

def calculate(operation_type, values):
    operators = { 
        'sum': add, 
        'sub': sub, 
        'mul': mul, 
        'div': truediv 
    }
    result = reduce(operators[operation_type], values)
    return result