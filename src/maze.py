from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum
from grid import Grid


class MazeCell(IntEnum):
    WALL = 0
    PATH = 1
    START = 2
    END = 3


class Maze:
    __grid: Grid[MazeCell]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.__grid = Grid[MazeCell](width, height, MazeCell.WALL)

    def get(self, x: int, y: int) -> MazeCell:
        return self.__grid.get(x, y)

    def set(self, x: int, y: int, value: MazeCell) -> None:
        self.__grid.set(x, y, value)

    def neighbors(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        if not self.in_bounds(x, y):
            raise ValueError("position outside maze")
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def walkable_neighbors(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        for nx, ny in self.neighbors(x, y):
            if self.get(nx, ny) != MazeCell.WALL:
                yield nx, ny

    def rows(self) -> Iterator[list[MazeCell]]:
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


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> MazePath: ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: Maze) -> None: ...


class MazeDisplayer:
    @staticmethod
    def display_ascii(maze: Maze, symbols: dict[MazeCell, str]) -> None:
        for row in maze.rows():
            print("".join(symbols[cell] for cell in row))
