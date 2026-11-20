import sys

from fdf.app import App
from fdf.errors import FdfError
from fdf.parser import parse_map


def main() -> int:
    """Главная функция программы."""

    if len(sys.argv) != 2:
        print(
            "Использование: python main.py <файл.fdf>",
            file=sys.stderr
        )
        return 2

    file_path = sys.argv[1]

    try:
        map_data = parse_map(file_path)

    except OSError as error:
        print(f"Ошибка чтения файла: {error}", file=sys.stderr)
        return 1

    except FdfError as error:
        print(f"Ошибка формата карты: {error}", file=sys.stderr)
        return 1

    app = App(map_data)
    app.run()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())