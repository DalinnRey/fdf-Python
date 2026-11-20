from pathlib import Path

from fdf.errors import MapFormatError
from fdf.model import Map, Point


def _parse_value(
    token: str,
    line: int,
    column: int
) -> tuple[int, str | None]:
    """Разбирает высоту и необязательный цвет точки."""

    parts = token.split(",")

    if len(parts) > 2:
        raise MapFormatError(
            f"строка {line}, колонка {column}: "
            f"{token!r} — некорректный цвет"
        )

    try:
        height = int(parts[0])
    except ValueError as exc:
        raise MapFormatError(
            f"строка {line}, колонка {column}: "
            f"{token!r} — не целое число"
        ) from exc

    color = None

    if len(parts) == 2:
        color_text = parts[1]

        if not color_text.lower().startswith("0x"):
            raise MapFormatError(
                f"строка {line}, колонка {column}: "
                f"{token!r} — некорректный цвет"
            )

        hex_value = color_text[2:]
        valid_digits = "0123456789abcdefABCDEF"

        if not 1 <= len(hex_value) <= 6:
            raise MapFormatError(
                f"строка {line}, колонка {column}: "
                f"{token!r} — некорректный цвет"
            )

        if any(char not in valid_digits for char in hex_value):
            raise MapFormatError(
                f"строка {line}, колонка {column}: "
                f"{token!r} — некорректный цвет"
            )

        color = f"#{int(hex_value, 16):06X}"

    return height, color


def parse_map(path: str | Path) -> Map:
    """Читает файл FDF и возвращает модель карты."""

    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()

    # Убираем пустые строки только в конце файла.
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        raise MapFormatError("Файл карты пуст")

    points: list[list[Point]] = []
    expected_width: int | None = None

    for y, line in enumerate(lines):
        tokens = line.split()

        if not tokens:
            raise MapFormatError(
                f"строка {y + 1}, колонка 1: пустая строка внутри карты"
            )

        if expected_width is None:
            expected_width = len(tokens)

        elif len(tokens) != expected_width:
            column = min(len(tokens), expected_width) + 1
            raise MapFormatError(
                f"строка {y + 1}, колонка {column}: "
                f"ожидалось {expected_width} значений, "
                f"получено {len(tokens)}"
            )

        row: list[Point] = []

        for x, token in enumerate(tokens):
            height, color = _parse_value(token, y + 1, x + 1)

            point = Point(
                x=x,
                y=y,
                z=height,
                color=color
            )

            row.append(point)

        points.append(row)

    return Map(points)