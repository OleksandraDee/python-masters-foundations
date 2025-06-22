def get_cats_info(path):
    cats = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 3:
                    print(f"Пропущено некоректний рядок: {line.strip()}")
                    continue

                cat = {
                    "id": parts[0],
                    "name": parts[1],
                    "age": parts[2]
                }
                cats.append(cat)

        return cats

    except FileNotFoundError:
        print(f"Файл за шляхом '{path}' не знайдено.")
        return []


cats_info = get_cats_info("Chapter06/goit-pycore-hw-06/cats_file.txt")
print(cats_info)
