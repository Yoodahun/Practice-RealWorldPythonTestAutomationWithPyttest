from typing import Callable, List, Tuple

import pytest

from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached
from fibonacci.dynamic import fibonacci_dynamic, fibonacci_dynamic_v2
from fibonacci.naive import fibonacci_naive
from conftest import time_tracker


# Decorator = Callable
# def my_parameterize(identifiers: str, values: List[Tuple[int, int]]) -> Decorator:
#     def my_parameterized_decorator(function: Callable) -> Callable:
#         def run_func_parameterized():
#             list_of_kwargs_for_function = get_list_of_kwargs_for_function(
#                 identifiers=identifiers,
#                 values=values
#             )
#             for kwargs_for_function in list_of_kwargs_for_function:
#                 print(
#                     f"calling function {function.__name__} with {kwargs_for_function}"
#                 )
#                 function(**kwargs_for_function)
#
#     return my_parameterized_decorator

@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
# @my_parameterize(identifiers="n, expected", values=[(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_naive(n: int, expected: int):
    assert fibonacci_naive(n) == expected


@pytest.mark.parametrize("fib_func ", [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached, fibonacci_dynamic, fibonacci_dynamic_v2])
@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci(time_tracker, fib_func: Callable[[int], int], n: int, expected: int):
    res = fib_func(n)
    assert res == expected
