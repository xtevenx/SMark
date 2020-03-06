import math
import sys
from typing import Callable, List, Type

import stats

_MAX_PRECISION: float = sys.float_info.epsilon
_SCALE_FUNCTION: Type = Callable[[List[float], float], List[float]]


def scale(data: List[float], target: float, scale_func: _SCALE_FUNCTION
          ) -> (List[float], float):
    assert all(0 <= n <= 1 for n in data + [target])

    def scale_result(n: float) -> float:
        return stats.mean(scale_func(data, n))

    scale_factor = _binary_search(
        lower_bound=0,
        upper_bound=sys.maxsize,
        func=scale_result,
        target=target,
        precision=_MAX_PRECISION,
    )

    return scale_func(data, scale_factor), scale_factor


def inverse_power_scale(data: List[float], power: float) -> List[float]:
    return [1 - (1 - n) ** power for n in data]


def log_scale(data: List[float], power: float) -> List[float]:
    if power == 1.0:
        power += _MAX_PRECISION * (-1 * (random.random() > 0.5))

    return [math.log(((power - 1) / power) * n + (1 / power), power) + 1 for n in data]


def power_scale(data: List[float], power: float) -> List[float]:
    """
    Scale a sequence of numbers based on the `power_scale` method.

    The `power_scale` method is a variable tweak of the commonly used
    scaling method where one scales a score, 'n' {0 <= n <= 100}, by
    multiplying the square root of 'n' by a factor of 10, namely:

        n_{scaled} = 10 * (n_{original} ** (1/2))

    The `power_scale` allows the variation of the exponent (in the
    example, `1/2`) to achieve variable scaling rates.

    :param data: the sequence of floats of which to scale.
    :param power: the scaling factor. A number lower than one results
        in the numbers of the sequence being scaled upwards where a
        lower number represents more scaling. A number higher than one
        results in the numbers being scaled downwards where a higher
        number represents more scaling.
    :return: the sequence of numbers after scaling. The numbers in the
        sequence remain in the original order as they were given and
        the `data` is not modified.
    """

    return [n ** (1 / power) for n in data]


def _binary_search(lower_bound: float, upper_bound: float, func: Callable[[float], float],
                   target: float, precision: float = _MAX_PRECISION, reverse: bool = False
                   ) -> float:
    assert upper_bound > lower_bound

    search_iterations = math.log2((upper_bound - lower_bound) / precision)
    for _ in range(int(search_iterations + 1)):
        guess = (lower_bound + upper_bound) / 2
        answer = func(guess)

        if (not reverse and answer > target) or (reverse and target > answer):
            upper_bound = guess
        else:
            lower_bound = guess

    return (lower_bound + upper_bound) / 2


if __name__ == "__main__":
    import random

    DISPLAY_CUTOFF = 10


    def display_info(data: List[float]) -> None:
        if len(data) > DISPLAY_CUTOFF:
            print(
                "data:",
                ", ".join("{:.1f}%".format(100 * n) for n in data[:DISPLAY_CUTOFF]),
                " ..."
            )
        else:
            print("data:", ", ".join("{:.1f}%".format(100 * n) for n in data))
        print(f"mean: {round(100 * stats.mean(data), 1)}%")
        print(f"stddev: {round(100 * stats.stddev(data), 1)}%")


    L = [random.random() for _ in range(10000)]
    print("ORIGINAL:")
    display_info(L)

    formulae = (
        ("inverse_power_scale", inverse_power_scale),
        ("log_scale", log_scale),
        ("power_scale", power_scale),
    )

    for name, foo in formulae:
        temp_L, s_factor = scale(L, 0.7, foo)

        print()
        print(f"SCALED ({name.upper()}):")
        print(f"scale factor: {round(s_factor, 2)}")
        display_info(temp_L)
