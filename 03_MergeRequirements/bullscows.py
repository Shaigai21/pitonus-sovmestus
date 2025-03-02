from typing import Tuple
import random

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls = sum(g == s for g, s in zip(guess, secret))
    cows = sum(1 if c in secret else 0 for c in set(guess)) - bulls
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    attempts = 0
    
    while True:
        guess = ask("Введите слово: ", words)
        attempts += 1
        bulls, cows = bullscows(guess, secret_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        
        if guess == secret_word:
            return attempts

def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        word = input(prompt)
        if valid is None or word in valid:
            return word
        print("Недопустимое слово. Попробуйте еще раз.")

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))
