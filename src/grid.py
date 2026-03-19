from typing import Iterator
from bitarray import bitarray


class BinaryGrid:
    _grid: bitarray
    width: int
    height: int

    def __init__(
        self,
        dimensions: tuple[int, int],
        default: bool = True,
    ) -> None:
        self.width, self.height = dimensions
        if self.width <= 0 or self.height <= 0:
            raise ValueError("dimensions must be greater than 0")
        self._grid = bitarray(self.width * self.height)
        self._grid.setall(default)

    def _index(self, pos: tuple[int, int]) -> int:
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"coordinate ({x}, {y}) exceeds "
                f"bounds ({self.width}, {self.height})"
            )
        return y * self.width + x

    def get(self, pos: tuple[int, int]) -> bool:
        return bool(self._grid[self._index(pos)])

    def set(self, pos: tuple[int, int], value: bool) -> None:
        self._grid[self._index(pos)] = value

    def rows(self) -> Iterator[Iterator[bool]]:
        for y in range(self.height):
            start = y * self.width
            end = start + self.width
            yield (bool(v) for v in self._grid[start:end])
