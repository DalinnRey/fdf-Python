from fdf.model import Map, Point


def create_test_map() -> Map:
    """Создаёт небольшую карту 2×2 для тестирования."""
    points = [
        [
            Point(0, 0, 0),
            Point(1, 0, 1)
        ],
        [
            Point(0, 1, 2),
            Point(1, 1, 3)
        ]
    ]
    return Map(points)


def test_map_length() -> None:
    map_data = create_test_map()
    assert len(map_data) == 4


def test_map_width_and_height() -> None:
    map_data = create_test_map()
    assert map_data.width == 2
    assert map_data.height == 2


def test_map_iteration() -> None:
    map_data = create_test_map()
    assert len(list(map_data)) == 4


def test_corner_neighbors() -> None:
    map_data = create_test_map()
    point = map_data.points[0][0]

    neighbors = map_data.neighbors(point)

    assert len(neighbors) == 2


def test_empty_map() -> None:
    try:
        Map([])
    except ValueError:
        return

    raise AssertionError("Ожидалась ошибка ValueError")


def test_uneven_map() -> None:
    points = [
        [Point(0, 0, 0), Point(1, 0, 1)],
        [Point(0, 1, 2)]
    ]

    try:
        Map(points)
    except ValueError:
        return

    raise AssertionError("Ожидалась ошибка ValueError")