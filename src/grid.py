from typing import Iterator, TypeVar, Generic

T = TypeVar("T")


class Grid(Generic[T]):
    __grid: list[T]

    def __init__(self, width: int, height: int, default: T) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("dimensions must be greater than 0")

        self.width = width
        self.height = height
        self.__grid = [default] * (width * height)

    def _index(self, x: int, y: int) -> int:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"Invalid coordinate ({x}, {y})")
        return y * self.width + x

    def get(self, x: int, y: int) -> T:
        return self.__grid[self._index(x, y)]

    def set(self, x: int, y: int, value: T) -> None:
        self.__grid[y * self.width + x] = value

    def rows(self) -> Iterator[list[T]]:
        for y in range(self.height):
            start = y * self.width
            yield self.__grid[start:start + self.width]
