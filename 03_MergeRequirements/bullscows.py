from typing import Tuple

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(1 if c in secret else 0 for c in set(guess)) - bulls
    return bulls, cows