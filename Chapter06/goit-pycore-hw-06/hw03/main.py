import sys
from pathlib import Path
from colorama import init, Fore, Style

# Ініціалізація colorama
init()

def print_directory_tree(directory: Path, indent: str = ""):
    try:
        for item in directory.iterdir():
            if item.is_dir():
                print(indent + Fore.BLUE + f"📂 {item.name}" + Style.RESET_ALL)
                print_directory_tree(item, indent + "    ")
            else:
                print(indent + Fore.GREEN + f"📜 {item.name}" + Style.RESET_ALL)
    except PermissionError:
        print(indent + Fore.RED + "🚫 Доступ заборонено" + Style.RESET_ALL)

def main():
    if len(sys.argv) != 2:
        print("⚠️  Використання: python hw03.py <шлях_до_директорії>")
        return

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"❌ Шлях '{path}' не існує.")
        return

    if not path.is_dir():
        print(f"❌ Шлях '{path}' не є директорією.")
        return

    print(Fore.YELLOW + f"Структура директорії: {path}" + Style.RESET_ALL)
    print_directory_tree(path)

if __name__ == "__main__":
    main()
