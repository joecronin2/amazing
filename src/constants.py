# from dataclasses import dataclass


class Key:
    ESC = 65307
    SPACE = 32
    ENTER = 65293
    PLUS = 61
    MINUS = 45
    LEFT = 65361
    UP = 65362
    RIGHT = 65363
    DOWN = 65364


class Color:
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
                hex_color & 0xFF,
                (hex_color >> 8) & 0xFF,
                (hex_color >> 16) & 0xFF,
                (hex_color >> 24) & 0xFF,
            ]
        )
