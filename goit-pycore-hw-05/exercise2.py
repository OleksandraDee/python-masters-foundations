import re
from typing import Callable

def generator_numbers(text: str):
    pattern = r"(?<=\s)\d+\.\d+(?=\s)"
    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, func: Callable):
    return sum(func(text))

def run_income_counter():
    print("Введіть текст з доходами (в форматі: число.число).")
    print("Наприклад: '1000.00 зарплата 200.50 бонуси 50.00 чайові'")
    print("Щоб вийти, введіть 'exit' або 'quit'.\n")

    while True:
        text = input("Введіть текст >>> ")

        if text.lower() in ['exit', 'quit']:
            print("Завершення роботи.")
            break

        print("\nЗнайдені числа:")
        for number in generator_numbers(text):
            print(f"- {number}")

        total = sum_profit(text, generator_numbers)
        print(f"Загальний дохід: {total}\n")

if __name__ == "__main__":
    run_income_counter()