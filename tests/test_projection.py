import pytest

from fdf.model import Map, Point
from fdf.projection import Camera


def test_origin_projection() -> None:
    camera = Camera()

    result = camera.project(Point(0, 0, 0))

    assert result == (0.0, 0.0)


def test_height_moves_point_up() -> None:
    camera = Camera()

    result = camera.project(Point(0, 0, 1))

    assert result[1] < 0


def test_fit_points_inside_window() -> None:
    points = [
        [
            Point(x, y, (x + y) % 3)
            for x in range(5)
        ]
        for y in range(5)
    ]

    map_data = Map(points)
    camera = Camera()

    width = 800
    height = 600

    camera.fit(map_data, width, height)

    for point in map_data:
        x, y = camera.project(point)

        assert 0 <= x <= width
        assert 0 <= y <= height


def test_fit_centers_map() -> None:
    map_data = Map([
        [
            Point(0, 0, 0),
            Point(1, 0, 0)
        ],
        [
            Point(0, 1, 0),
            Point(1, 1, 0)
        ]
    ])

    camera = Camera()
    camera.fit(map_data, 800, 600)

    projected = [
        camera.project(point)
        for point in map_data
    ]

    center_x = (
        min(p[0] for p in projected) +
        max(p[0] for p in projected)
    ) / 2

    center_y = (
        min(p[1] for p in projected) +
        max(p[1] for p in projected)
    ) / 2

    assert center_x == pytest.approx(400)
    assert center_y == pytest.approx(300)


def test_fit_single_point() -> None:
    map_data = Map([[Point(0, 0, 0)]])

    camera = Camera()
    camera.fit(map_data, 800, 600)

    assert camera.project(map_data.points[0][0]) == (400, 300)


def test_fit_invalid_window() -> None:
    map_data = Map([[Point(0, 0, 0)]])
    camera = Camera()

    with pytest.raises(ValueError):
        camera.fit(map_data, 0, 600)