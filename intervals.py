import itertools # we'll need chain to join the iterables
# caution this breaks on Python less than 3.5.2!!!
import sympy
import math
import numpy as np
import code


def complement_perfect_squares(start, finish):
    start = round(start)
    finish = round(finish)
    not_perfect_squares = []
    for elem in range(start, finish+1):
        sq_root = math.pow(elem, 0.5)
        if sq_root != round(sq_root):
            not_perfect_squares.append(sq_root)
    for elem in not_perfect_squares:
        yield elem

    
def process_end_points(start, finish, include_start, include_finish, step_size):
    if not include_start:
        start += step_size
    if not include_finish:
        finish -= step_size
    return start, finish


def construct_naturals(start, finish, include_start, include_finish):
    step_size = 1
    start, finish = process_end_points(
        start, finish, include_start, include_finish, step_size)
    return range(start, finish+step_size)


def construct_rationals(start, finish, include_start, include_finish):
    step_size = 0.00001
    start, finish = process_end_points(
        start, finish, include_start, include_finish, step_size)
    return np.nditer(np.arange(start, finish+step_size, step=step_size))


def generate_iter_for_transcendental(transcendental, start, finish, step_size):
    # this case needs work
    if transcendental < start:
        return np.nditer(
            np.arange(
                transcendental,
                finish+step_size,
                step=step_size
            )
        )
    # this case needs work
    elif transcendental > finish:
        return np.nditer(
            np.arange(
                start,
                transcendental,
                step=step_size
            )
        )

    else:
        return itertools.chain(
            # this case needs work
            np.nditer(np.arange(start, transcendental, step=step_size)),
            # this case doesn't need work
            np.nditer(np.arange(transcendental, finish+step_size, step=step_size))
        )

    
def construct_irrationals(start, finish, include_start, include_finish):
    step_size = 0.00001
    start, finish = process_end_points(
        start, finish, include_start, include_finish, step_size)
    pi = float(sympy.N(sympy.pi, 100))
    E = float(sympy.N(sympy.E, 100))
    golden_ratio = float(sympy.N(sympy.GoldenRatio, 100))
    not_perfect_squares = complement_perfect_squares(start, finish)
    pi_iter = generate_iter_for_transcendental(
        pi, start, finish, step_size)
    E_iter = generate_iter_for_transcendental(
        E, start, finish, step_size)
    golden_ratio_iter = generate_iter_for_transcendental(
        golden_ratio, start, finish, step_size)
    not_perfect_squares = [np.nditer(np.arange(elem, finish, step=step_size))
                           for elem in not_perfect_squares]
    iterator = itertools.chain(pi_iter, E_iter)
    iterator = itertools.chain(iterator, golden_ratio_iter)
    for item in not_perfect_squares:
        iterator = itertools.chain(iterator, item)
    return iterator


def a_range(start, finish, how="(,)"):
    """
    a_range constructs intervals over the real numbers.
    You can pass anything you might like.
    
    """
    begin, end = how.split(",")

    if begin == "(":
        include_start = False
    else:
        include_start = True
        
    if end == ")":
        include_finish = False
    else:
        include_finish = True
    naturals = construct_naturals(start, finish, include_start, include_finish)
    rationals = construct_rationals(start, finish, include_start, include_finish)
    irrationals = construct_irrationals(start, finish, include_start, include_finish)
    iterator = itertools.chain(naturals, rationals)
    iterator = itertools.chain(iterator, irrationals)
    return sorted(iterator)


if __name__ == '__main__':
    result = a_range(1, 2)
    code.interact(local=locals())
    
