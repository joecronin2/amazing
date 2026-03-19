import mlx
from typing import Any
from dataclasses import dataclass

from maze import Maze


class Color:
    # 0xAARRGGBB Format
    BLACK = 0xFF000000
    WHITE = 0xFFFFFFFF
    RED = 0xFFFF0000
    GREEN = 0xFF00FF00
    BLUE = 0xFF0000FF
    YELLOW = 0xFFFFFF00
    PURPLE = 0xFF800080
    GREY = 0xFF808080

    @staticmethod
    def to_bytes(hex_color: int) -> bytes:
        return bytes(
            [
                hex_color & 0xFF,  # B
                (hex_color >> 8) & 0xFF,  # G
                (hex_color >> 16) & 0xFF,  # R
                (hex_color >> 24) & 0xFF,  # A
            ]
        )

    @staticmethod
    def from_rgb(r: int, g: int, b: int, a: int = 255) -> int:
        return (a << 24) | (r << 16) | (g << 8) | b


@dataclass
class ImageBuffer:
    ptr: Any
    buffer: memoryview
    line_len: int
    bpp: int
    width: int
    height: int

    @classmethod
    def from_mlx(cls, app, img_ptr: Any, width: int, height: int):
        addr, bpp, line_len, _ = app.mlx_get_data_addr(img_ptr)
        return cls(
            ptr=img_ptr,
            buffer=addr,
            bpp=bpp,
            line_len=line_len,
            width=width,
            height=height,
        )

    @property
    def bytes_per_pixel(self) -> int:
        return self.bpp // 8

    def _get_offset(self, x: int, y: int) -> int:
        return (y * self.line_len) + (x * self.bytes_per_pixel)

    def _is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def put_pixel(self, x: int, y: int, pixel_bytes: bytes) -> None:
        if self._is_in_bounds(x, y):
            start = self._get_offset(x, y)
            self.buffer[start : start + self.bytes_per_pixel] = pixel_bytes

    def draw_row(
        self,
        x: int,
        y: int,
        length: int,
        pixel_bytes: bytes,
    ) -> None:
        if not (0 <= y < self.height):
            return
        start_x = max(0, x)
        end_x = min(self.width, x + length)
        if start_x >= end_x:
            return
        actual_len = end_x - start_x
        offset_start = self._get_offset(start_x, y)
        offset_end = offset_start + (actual_len * self.bytes_per_pixel)
        self.buffer[offset_start:offset_end] = pixel_bytes * actual_len


class MlxAPI:
    def __init__(self) -> None:
        self.app = mlx.Mlx()
        self.mlx_ptr = self.app.mlx_init()
        self.windows = []
        self.images = []

        if not self.mlx_ptr:
            raise RuntimeError("failed to initialize MiniLibX")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        for win in self.windows:
            self.app.mlx_destroy_window(self.mlx_ptr, win)
        for img in self.images:
            self.app.mlx_destroy_image(self.mlx_ptr, img.ptr)
        self.windows.clear()
        self.images.clear()

    def create_window(self, size: tuple[int, int], title: str) -> Any:
        w, h = size
        win = self.app.mlx_new_window(self.mlx_ptr, w, h, title)
        self.windows.append(win)
        return win

    def create_image(self, width: int, height: int) -> ImageBuffer:
        img_ptr = self.app.mlx_new_image(self.mlx_ptr, width, height)
        img_buf = ImageBuffer.from_mlx(self.app, img_ptr, width, height)
        self.images.append(img_buf)
        return img_buf

    def set_hook(self, win, event: int, mask: int, callback, param=None):
        self.app.mlx_hook(win, event, mask, callback, param)

    def on_key_down(self, win, callback, param=None):
        self.set_hook(win, 2, 1 << 0, callback, param)

    def on_close(self, win, callback, param=None):
        self.set_hook(win, 17, 0, callback, param)

    def display(self, window, img: ImageBuffer, x: int = 0, y: int = 0):
        self.app.mlx_put_image_to_window(self.mlx_ptr, window, img.ptr, x, y)

    def on_loop(self, callback, param=None):
        self.app.mlx_loop_hook(self.mlx_ptr, callback, param)

    def loop(self):
        self.app.mlx_loop(self.mlx_ptr)

    def loop_exit(self):
        self.app.mlx_loop_exit(self.mlx_ptr)


class MlxMazeRenderer:
    def __init__(
        self,
        api: MlxAPI,
        window: Any,
        maze: Maze,
        cell_size: int = 20,
    ) -> None:
        self.api = api
        self.window = window
        self.maze = maze
        self.cell_size = cell_size
        width = self.maze.width * self.cell_size
        height = self.maze.height * self.cell_size
        self._img = self.api.create_image(width, height)

    def _get_color(self, pos: tuple[int, int], path_set: set) -> int:
        if pos == self.maze.start:
            return Color.GREEN
        if pos == self.maze.end:
            return Color.RED
        if self.maze.is_wall(pos):
            return Color.BLACK
        if pos in path_set:
            return Color.BLUE
        return Color.WHITE

    def _draw_cell(self, x: int, y: int, color: int) -> None:
        px, py = x * self.cell_size, y * self.cell_size
        pixel_bytes = Color.to_bytes(color)
        for row_offset in range(self.cell_size):
            self._img.draw_row(px, py + row_offset, self.cell_size, pixel_bytes)

    def render(self) -> None:
        path_set = set(self.maze.path) if self.maze.path else set()
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                color = self._get_color((x, y), path_set)
                self._draw_cell(x, y, color)
        self.api.display(self.window, self._img)
