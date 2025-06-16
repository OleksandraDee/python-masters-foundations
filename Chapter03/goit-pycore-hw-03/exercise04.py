from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    upcoming_birthdays = []

    for user in users:
        # Конвертація дня народження з рядка
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=today.year)

        # Якщо вже минув у цьому році — беремо наступний рік
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # Перевіряємо, чи в межах наступних 7 днів
        if today <= birthday_this_year <= end_date:
            congratulation_date = birthday_this_year

            # Якщо вихідний — переносимо на наступний понеділок
            if congratulation_date.weekday() in (5, 6):  # 5 = субота, 6 = неділя
                days_until_monday = 7 - congratulation_date.weekday()
                congratulation_date += timedelta(days=days_until_monday)

            # Додаємо до списку результатів
            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays

# Приклад використання

users = [
    {"name": "John Doe", "birthday": "1985.06.23"},
    {"name": "Jane Smith", "birthday": "1990.06.27"},
    {"name": "Bob White", "birthday": "1992.06.28"}
]

upcoming = get_upcoming_birthdays(users)
print("Список привітань на цьому тижні:", upcoming)

# Вивід:
# Список привітань на цьому тижні: [{'name': 'John Doe', 'congratulation_date': '2025.06.23'}]