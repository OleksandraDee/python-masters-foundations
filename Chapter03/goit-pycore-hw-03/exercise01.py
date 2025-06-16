from datetime import datetime

def get_days_from_today(date):
    try:
        input_date = datetime.strptime(date, '%Y-%m-%d').date()
        today_date = datetime.today().date()
        delta = (today_date - input_date).days
        return delta
    except ValueError:
        print("Неправильний формат дати. Використовуйте 'YYYY-MM-DD'.")
        return None

# Функція для опису різниці в днях
def describe_date_difference(days):
    if days > 0:
        return f"Ця дата була {days} днів тому."
    elif days < 0:
        return f"Ця дата буде через {abs(days)} днів."
    else:
        return "Ця дата — сьогодні."

# Основний виклик
string_date = input("Введіть дату у форматі 'YYYY-MM-DD': ")
days = get_days_from_today(string_date)

if days is not None:
    message = describe_date_difference(days)
    print(message)
