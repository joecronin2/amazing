from typing import Iterator


class BinaryGrid:
    __grid: list[bool]

    def __init__(self, width: int, height: int, default: bool = True) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("dimensions must be greater than 0")

        self.width = width
        self.height = height
        self.__grid = [default] * (width * height)

    def _index(self, x: int, y: int) -> int:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"invalid coordinate ({x}, {y})")
        return y * self.width + x

    def get(self, x: int, y: int) -> bool:
        """True = wall, False = open"""
        return self.__grid[self._index(x, y)]

    def set(self, x: int, y: int, value: bool) -> None:
        self.__grid[self._index(x, y)] = value

    def rows(self) -> Iterator[list[bool]]:
        for y in range(self.height):
            start = y * self.width
            yield self.__grid[start:start + self.width]
