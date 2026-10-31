
import random


def roll_d100() -> int:
    """
    Genera una tirada aleatoria de percentiles
    entre 1 y 100.
    """
    return random.randint(1, 100)
