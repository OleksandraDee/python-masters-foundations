import random

def get_numbers_ticket(min, max, quantity):
    # Перевірка вхідних параметрів, щоб вони були цілими числами
    # та відповідали умовам
    if (
        not isinstance(min, int) or
        not isinstance(max, int) or
        not isinstance(quantity, int)
    ):
        return []

    if min < 1 or max > 1000:
        return []

    if quantity < 1 or quantity > (max - min + 1):
        return []

    numbers = random.sample(range(min, max + 1), quantity)
    return sorted(numbers)

print("=== Генератор лотерейних чисел ===")
print("Ви зараз введете три значення:")
print(" - Мінімальне число (не менше 1)")
print(" - Максимальне число (не більше 1000)")
print(" - Кількість чисел, які потрібно обрати")

try:
    min_num = int(input("Введіть мінімальне число: "))
    max_num = int(input("Введіть максимальне число: "))
    qty = int(input("Скільки чисел потрібно згенерувати?: "))

    ticket = get_numbers_ticket(min_num, max_num, qty)

    if ticket:
        print("Ваші лотерейні числа:", ticket)
    else:
        print("Невірні параметри. Перевірте, чи числа вірні і не суперечать правилам.")

except ValueError:
    print("Помилка: потрібно вводити лише цілі числа.")