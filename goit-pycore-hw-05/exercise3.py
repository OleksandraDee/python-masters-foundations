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

def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return counts

def display_log_counts(counts: dict):
    print(f"{'Log Level':<15} | {'Count':<5}")
    print("-" * 25)
    for level, count in counts.items():
        print(f"{level:<15} | {count:<5}")

def main():
    file_path = r"logs.txt"

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

if __name__ == "__main__":
    main()
