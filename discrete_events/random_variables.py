from numpy import random
from math import e, log, sqrt


def generate_client():
    u = random.uniform(0, 1)
    if u <= 0.45:
        return 1
    if 0.45 < u <= 0.70:
        return 2
    if 0.70 < u <= 0.80:
        return 3
    if 0.80 < u <= 1:
        return 4


def poisson(lam):
    n = 0
    u = random.uniform(0, 1)
    while u >= e ** (-lam):
        u *= random.uniform(0, 1)
        n += 1
    return n


def exponential(lam):
    u = random.uniform(0, 1)
    return -(1 / lam) * log(u, e)


def normal(mu=5, sigma=2):
    u = random.uniform(0, 1)
    y1 = 0
    y2 = 0
    while y2 - (((y1 - 1) ** 2) / 2) <= 0:
        y1 = exponential(1)
        y2 = exponential(1)
    u = random.uniform(0, 1)
    ret = y1 if u > 0.5 else -y1
    return ret * sqrt(sigma) + mu
