import tkinter as tk

from fdf.model import Map
from fdf.projection import Camera


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

    def _on_resize(self, _event: tk.Event) -> None:
        """Пересчитывает проекцию при изменении размера окна."""

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        self.camera.fit(self.map_data, width, height)
        self._draw()

    def _draw(self) -> None:
        """Рисует каркас карты."""

        self.canvas.delete("all")

        for y, row in enumerate(self.map_data.points):
            for x, point in enumerate(row):

                x1, y1 = self.camera.project(point)

                # Соединяем с точкой справа
                if x + 1 < self.map_data.width:
                    right = self.map_data.points[y][x + 1]
                    x2, y2 = self.camera.project(right)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#DDE7F0",
                        width=2
                    )

                # Соединяем с точкой снизу
                if y + 1 < self.map_data.height:
                    below = self.map_data.points[y + 1][x]
                    x2, y2 = self.camera.project(below)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="#DDE7F0",
                        width=2
                    )