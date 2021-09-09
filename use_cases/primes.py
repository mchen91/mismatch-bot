import itertools


def is_prime(n):
    if n < 4:
        return True
    for d in itertools.chain([2], itertools.count(3, 2)):
        if n % d == 0:
            return False
        if d * d > n:
            return True
