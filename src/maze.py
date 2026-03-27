from abc import ABC, abstractmethod
from collections.abc import Iterator
from grid import BinaryGrid


class Maze:
    __grid: BinaryGrid
    masked: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.width, self.height = dimensions
        self.__grid = BinaryGrid(dimensions, True)  # True is wall

    def set_start(self, pos: tuple[int, int]) -> None:
        self.start = pos
        self.set_open(pos)

    def set_end(self, pos: tuple[int, int]) -> None:
        self.end = pos
        self.set_open(pos)

    def is_wall(self, pos: tuple[int, int]) -> bool:
        return self.__grid.get(pos)

    def set_wall(self, pos: tuple[int, int]) -> None:
        self.__grid.set(pos, True)

    def set_open(self, pos: tuple[int, int]) -> None:
        self.__grid.set(pos, False)

    def neighbors(self, pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        if not self.in_bounds(pos):
            raise ValueError("position outside maze")
        x, y = pos
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if self.in_bounds((nx, ny)) and (nx, ny):
                yield nx, ny

    def open_neighbors(
        self,
        pos: tuple[int, int],
    ) -> Iterator[tuple[int, int]]:
        for neighbor in self.neighbors(pos):
            if not self.is_wall(neighbor):
                yield neighbor

    def rows(self) -> Iterator[Iterator[bool]]:
        return self.__grid.rows()

    def _pos_ascii(self, pos: tuple[int, int]) -> str:
        if pos == self.start:
            return "s"
        elif pos == self.end:
            return "e"
        # elif pos in self.path:
        #     return "."
        elif self.is_wall(pos):
            return "#"
        return " "

    def __str__(self) -> str:
        return "\n".join(
            "".join(self._pos_ascii((x, y)) for x, _ in enumerate(row))
            for y, row in enumerate(self.rows())
        )


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self, dimensions: tuple[int, int]) -> Maze: ...


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> list[tuple[int, int]]: ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: Maze) -> None: ...
