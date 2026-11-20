from dataclasses import dataclass
from math import cos, radians, sin

from fdf.model import Map, Point


@dataclass
class Camera:
    """Камера для преобразования координат карты."""

    scale: float = 1.0
    offset_x: float = 0.0
    offset_y: float = 0.0
    z_scale: float = 1.0

    def _project_base(self, point: Point) -> tuple[float, float]:
        """Вычисляет изометрические координаты без масштаба и смещения."""

        angle = radians(30)

        x_prime = (point.x - point.y) * cos(angle)
        y_prime = (point.x + point.y) * sin(angle) - point.z * self.z_scale

        return x_prime, y_prime

    def project(self, point: Point) -> tuple[float, float]:
        """Преобразует точку карты в координаты экрана."""

        x_prime, y_prime = self._project_base(point)

        screen_x = x_prime * self.scale + self.offset_x
        screen_y = y_prime * self.scale + self.offset_y

        return screen_x, screen_y

    def fit(self, map_data: Map, width: int, height: int) -> None:
        """Подбирает масштаб и смещение для размещения карты в окне."""

        if width <= 0 or height <= 0:
            raise ValueError("Размеры окна должны быть положительными")

        projected = [
            self._project_base(point)
            for point in map_data
        ]

        min_x = min(point[0] for point in projected)
        max_x = max(point[0] for point in projected)

        min_y = min(point[1] for point in projected)
        max_y = max(point[1] for point in projected)

        map_width = max_x - min_x
        map_height = max_y - min_y

        scale_x = (
            width * 0.9 / map_width
            if map_width > 0 else float("inf")
        )

        scale_y = (
            height * 0.9 / map_height
            if map_height > 0 else float("inf")
        )

        self.scale = min(scale_x, scale_y)

        if self.scale == float("inf"):
            self.scale = 1.0

        self.offset_x = (
            width / 2 - (min_x + max_x) / 2 * self.scale
        )

        self.offset_y = (
            height / 2 - (min_y + max_y) / 2 * self.scale
        )