from abc import ABC, abstractmethod
from collections.abc import Iterator
from grid import BinaryGrid


class Maze:
    __grid: BinaryGrid
    width: int
    height: int
    masked: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]

    def in_bounds(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.width, self.height = dimensions
        self.__grid = BinaryGrid(dimensions, True)  # True is wall

    def set_masked(self, masked: set[tuple[int, int]]) -> None:
        self.masked = masked

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

    def bin_neighbors(
            self,
            pos: tuple[int, int],
    ) -> int:
        n = 0
        x, y = pos
        if self.in_bounds([x, y-1]):
            if self.__grid.get([x, y-1]):
                n += 1
        else:
            n += 1

        if self.in_bounds([x+1, y]):
            if self.__grid.get([x+1, y]):
                n += 2
        else:
            n += 2

        if self.in_bounds([x, y+1]):
            if self.__grid.get([x, y+1]):
                n += 4
        else:
            n += 4

        if self.in_bounds([x-1, y]):
            if self.__grid.get([x-1, y]):
                n += 8
        else:
            n += 8
        return n

    def rows(self) -> Iterator[Iterator[bool]]:
        return self.__grid.rows()

    def __str__(self) -> str:
        # walls, start, end, masked
        def cell_repr(pos: tuple[int, int]) -> str:
            if pos == self.start:
                return "S"
            elif pos == self.end:
                return "E"
            elif pos in self.masked:
                return "X"
            elif self.is_wall(pos):
                return "#"
            else:
                return " "

        return "\n".join(
            "".join(cell_repr((x, y)) for x in range(self.width))
            for y in range(self.height)
        )

    def __repr__(self) -> str:
        return f"Maze({self.width}x{self.height})"


class MazeGenerator(ABC):
    @abstractmethod
    def generate(self, dimensions: tuple[int, int]) -> Maze: ...


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> list[tuple[int, int]]: ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, maze: Maze) -> None: ...
