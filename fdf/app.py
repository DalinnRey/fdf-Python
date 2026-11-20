import tkinter as tk

# Импортируем Map для работы с картой и Point для работы с отдельными точками.
from fdf.model import Map, Point
from fdf.projection import Camera

# Стандартный цвет линий, если у точки не указан собственный цвет.
DEFAULT_LINE_COLOR = "#DDE7F0"


def _get_edge_color(point: Point, neighbor: Point) -> str:
    """Определяет цвет линии между двумя соседними точками."""

    # Проверяем, есть ли цвет у первой точки.
    if point.color is None:

        # Если цвета нет у обеих точек, возвращаем стандартный.
        if neighbor.color is None:
            return DEFAULT_LINE_COLOR

        # Если цвет есть только у соседней точки, используем его.
        return neighbor.color

    # Если цвет есть только у первой точки, используем его.
    if neighbor.color is None:
        return point.color

    # Если у обеих точек разные цвета, сравниваем их высоты.
    if point.z >= neighbor.z:

        # Используем цвет точки, которая находится выше.
        return point.color

    # Если соседняя точка выше, используем её цвет.
    return neighbor.color


class App:
    """Графический интерфейс программы FdF."""

    def __init__(self, map_data: Map) -> None:
        self.map_data = map_data
        self.camera = Camera()

        # Создаём главное окно
        self.root = tk.Tk()
        self.root.title("FdF - Каркасная 3D-модель")
        self.root.geometry("900x700")

        # Создаём область для рисования
        self.canvas = tk.Canvas(
            self.root,
            background="#101820",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Обработка изменения размера окна
        self.canvas.bind("<Configure>", self._on_resize)

        # Завершение программы по Esc
        self.root.bind("<Escape>", self._on_escape)
        # Увеличение и уменьшение масштаба.
        # Основная клавиатура и цифровой блок.
        self.root.bind("<plus>", self._on_zoom_in)
        self.root.bind("<minus>", self._on_zoom_out)
        self.root.bind("<KP_Add>", self._on_zoom_in)
        self.root.bind("<KP_Subtract>", self._on_zoom_out)

        # Перемещение модели стрелками клавиатуры.
        self.root.bind("<Left>", self._on_move_left)
        self.root.bind("<Right>", self._on_move_right)
        self.root.bind("<Up>", self._on_move_up)
        self.root.bind("<Down>", self._on_move_down)

        # Завершение программы при закрытии окна
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.root.destroy
        )

    def run(self) -> None:
        """Запускает графическое окно."""
        self.root.mainloop()

    def _on_escape(self, _event: tk.Event) -> None:
        """Закрывает программу при нажатии Esc."""
        self.root.destroy()

    def _on_zoom_in(self, _event: tk.Event) -> None:
        """Увеличивает масштаб модели."""

        # Увеличиваем пользовательский масштаб на 10%.
        self.camera.zoom(1.1)

        # Пересчитываем положение модели и перерисовываем её.
        self._update_view()

    def _on_zoom_out(self, _event: tk.Event) -> None:
        """Уменьшает масштаб модели."""

        # Уменьшаем масштаб примерно на 9,1%.
        self.camera.zoom(1 / 1.1)

        # Пересчитываем положение модели и перерисовываем её.
        self._update_view()

    def _on_move_left(self, _event: tk.Event) -> None:
        """Перемещает модель влево."""
        self.camera.move(-20, 0)
        self._draw()

    def _on_move_right(self, _event: tk.Event) -> None:
        """Перемещает модель вправо."""
        self.camera.move(20, 0)
        self._draw()

    def _on_move_up(self, _event: tk.Event) -> None:
        """Перемещает модель вверх."""
        self.camera.move(0, -20)
        self._draw()

    def _on_move_down(self, _event: tk.Event) -> None:
        """Перемещает модель вниз."""
        self.camera.move(0, 20)
        self._draw()

    def _on_resize(self, _event: tk.Event) -> None:
        """Обрабатывает изменение размера окна."""

        # При изменении размера окна обновляем положение модели.
        self._update_view()

    def _update_view(self) -> None:
        """Пересчитывает камеру и перерисовывает модель."""

        # Получаем текущие размеры области рисования.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Не выполняем расчёты, если размеры ещё не определены.
        if width <= 1 or height <= 1:
            return

        # Подгоняем модель под окно с учётом Zoom и сдвига.
        self.camera.fit(self.map_data, width, height)

        # Рисуем модель заново.
        self._draw()

    def _draw(self) -> None:
        """Рисует каркас карты."""

        self.canvas.delete("all")

        for y, row in enumerate(self.map_data.points):
            # Перебираем каждую точку в текущей строке.
            for x, point in enumerate(row):
                 # Переводим координаты точки в координаты окна.
                x1, y1 = self.camera.project(point)

                # Соединяем с точкой справа
                if x + 1 < self.map_data.width:
                    right = self.map_data.points[y][x + 1]
                    edge_color = _get_edge_color(point, right)
                    x2, y2 = self.camera.project(right)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=edge_color,
                        width=2
                    )

                # Соединяем с точкой снизу
                if y + 1 < self.map_data.height:
                    below = self.map_data.points[y + 1][x]
                    edge_color = _get_edge_color(point, below)
                    x2, y2 = self.camera.project(below)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill=edge_color,
                        width=2
                    )