def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci

def run_fibonacci_console():
    fib = caching_fibonacci()
    print("Введіть число для обчислення n-го числа Фібоначчі.")
    print("Для виходу введіть 'exit', 'close' або 'quit'.")

    while True:
        user_input = input("Введіть число: ").strip().lower()

        if user_input in ['exit', 'close', 'quit']:
            print("Завершення роботи.")
            break

        if not user_input.isdigit():
            print("Будь ласка, введіть ціле додатнє число.")
            continue

        n = int(user_input)
        result = fib(n)
        print(f"F({n}) = {result}")

if __name__ == "__main__":
    run_fibonacci_console()


