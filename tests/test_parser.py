from pathlib import Path

import pytest

from fdf.errors import MapFormatError
from fdf.parser import parse_map


@pytest.mark.parametrize(
    ("value", "expected_z", "expected_color"),
    [
        ("7", 7, None),
        ("-3", -3, None),
        ("2,0xFF8800", 2, "#FF8800"),
        ("1,0xff", 1, "#0000FF"),
    ],
)
def test_parse_values(
    tmp_path: Path,
    value: str,
    expected_z: int,
    expected_color: str | None,
) -> None:
    file = tmp_path / "test.fdf"
    file.write_text(value, encoding="utf-8")

    result = parse_map(file)
    point = result.points[0][0]

    assert point.z == expected_z
    assert point.color == expected_color


def test_parse_elem_map() -> None:
    result = parse_map("maps/elem.fdf")

    assert result.width == 5
    assert result.height == 5
    assert result.points[2][2].z == 5


@pytest.mark.parametrize(
    "content",
    [
        "",
        "1 x",
        "1 2\n3",
        "1,0xGG",
    ],
)


def test_invalid_maps(tmp_path: Path, content: str) -> None:
    file = tmp_path / "bad.fdf"
    file.write_text(content, encoding="utf-8")

    with pytest.raises(MapFormatError):
        parse_map(file)


def test_parse_map_invalid_encoding(tmp_path: Path) -> None:
    """Проверяет обработку файла с неправильной кодировкой."""

    # Создаём временный файл для тестирования.
    file = tmp_path / "invalid_encoding.fdf"

    # Записываем байт, который не является допустимым UTF-8.
    file.write_bytes(b"\xff")

    # Проверяем, что парсер выдаёт нашу ошибку MapFormatError, а не необработанную ошибку UnicodeDecodeError.
    with pytest.raises(MapFormatError, match="UTF-8"):
        parse_map(file)