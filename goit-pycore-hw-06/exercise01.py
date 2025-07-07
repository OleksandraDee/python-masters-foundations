def total_salary(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            total = 0
            count = 0

            for line in file:
                line = line.strip()
                if not line:
                    continue  

                try:
                    _, salary = line.split(',')
                    total += int(salary)
                    count += 1
                except ValueError:
                    print(f"Увага: неможливо обробити рядок: '{line}'")

            if count == 0:
                return (0, 0)
            average = total / count
            return (total, average)

    except FileNotFoundError:
        print(f"Файл за шляхом '{path}' не знайдено.")
        return (0, 0)

total, average = total_salary("Chapter06/goit-pycore-hw-06/salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

# Загальна сума заробітної плати: 6000, Середня заробітна плата: 2000.0