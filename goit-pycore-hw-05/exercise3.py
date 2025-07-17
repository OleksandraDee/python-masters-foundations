import sys
from collections import defaultdict

def parse_log_line(line: str) -> dict:
    parts = line.strip().split(' ')
    date, time, level = parts[0], parts[1], parts[2]
    message = ' '.join(parts[3:])
    return {"date": date, "time": time, "level": level, "message": message}

def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                logs.append(parse_log_line(line))
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log['level'].lower() == level.lower(), logs))

def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return counts

def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<18} | {'Кількість':<8}")
    print("-" * 30)
    for level, count in counts.items():
        print(f"{level:<18} | {count:<8}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python log_parser.py <шлях до файлу> [<рівень>]")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        if filtered_logs:
            print(f"\nДеталі логів для рівня '{level.upper()}':")
            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"\nЛогів для рівня '{level.upper()}' не знайдено.")

if __name__ == "__main__":
    main()
