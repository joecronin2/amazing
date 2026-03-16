from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from grid import BinaryGrid


class Maze:
    __grid: BinaryGrid
    start: tuple[int, int]
    end: tuple[int, int]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def __init__(self, width: int, height: int) -> None:
        self.__grid = BinaryGrid(width, height, True)  # True is wall
        self.width = width
        self.height = height

    def set_start(self, x: int, y: int) -> None:
        self.start = (x, y)
        self.set_open(x, y)

    def set_end(self, x: int, y: int) -> None:
        self.end = (x, y)
        self.set_open(x, y)

    def is_wall(self, x: int, y: int) -> bool:
        return self.__grid.get(x, y)

    def set_wall(self, x: int, y: int) -> None:
        self.__grid.set(x, y, True)

    def set_open(self, x: int, y: int) -> None:
        self.__grid.set(x, y, False)

    def neighbors(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        if not self.in_bounds(x, y):
            raise ValueError("position outside maze")
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def open_neighbors(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        for nx, ny in self.neighbors(x, y):
            if not self.is_wall(nx, ny):
                yield nx, ny

    def rows(self) -> Iterator[list[bool]]:
        return self.__grid.rows()


@dataclass
class MazePath:
    cells: list[tuple[int, int]]

    def add(self, x: int, y: int) -> None:
        self.cells.append((x, y))

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def start(self):
        return self.cells[0]

    def end(self):
        return self.cells[-1]


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self, width: int, height: int) -> Maze: ...


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> MazePath: ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: Maze) -> None: ...


# class MazeDisplayer:
#     @staticmethod
#     def display_ascii(maze: Maze, symbols: dict[MazeCell, str]) -> None:
#         for row in maze.rows():
#             print("".join(symbols[cell] for cell in row))
