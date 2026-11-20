from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """Точка трёхмерной карты. Где x и y - координаты на карте, z - высота в этой точке, color - цвет точки."""

    x: int
    y: int
    z: int
    color: str | None = None


class Map:
    """Модель карты высот."""

    def __init__(self, points: list[list[Point]]) -> None:
        if not points or not points[0]:
            raise ValueError("Карта не может быть пустой")

        width = len(points[0])

        if any(len(row) != width for row in points):
            raise ValueError("Все строки карты должны иметь одинаковую длину")

        self.points = points
        self.width = width
        self.height = len(points)

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Point]:
        for row in self.points:
            yield from row

    def neighbors(self, point: Point) -> list[Point]:
        """Возвращает соседние точки по горизонтали и вертикали."""

        if not (0 <= point.x < self.width and
                0 <= point.y < self.height):
            raise ValueError("Точка находится за пределами карты")

        result: list[Point] = []

        if point.x > 0:
            result.append(self.points[point.y][point.x - 1])

        if point.x < self.width - 1:
            result.append(self.points[point.y][point.x + 1])

        if point.y > 0:
            result.append(self.points[point.y - 1][point.x])

        if point.y < self.height - 1:
            result.append(self.points[point.y + 1][point.x])

        return result