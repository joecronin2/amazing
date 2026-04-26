from io import TextIOWrapper
import sys
from maze import Maze
from game import MazeGame


def herecouldvebeensomeerrorhandling() -> None:
    exit()


def parse_coord(s: str) -> tuple[int, int]:
    pass


def parse_bool(s: str) -> bool:
    pass


def parse_input(f: TextIOWrapper) -> None:
    parsing_table = [["WIDTH=", int()],
                     ["HEIGHT=", int()],
                     ["ENTRY=", parse_coord()],
                     ["EXIT=", parse_coord()],
                     ["OUTPUT_FILE=", str()],
                     ["PERFECT=", parse_bool()]]

    i = 0
    for line in f:
        if line[0] == '#':
            continue
        if not line.startswith(parsing_table[i][0]):
            herecouldvebeensomeerrorhandling()
        s = line.removeprefix(parsing_table[i][0])


def handle_input_open() -> None:
    if len(sys.argv) != 2:
        herecouldvebeensomeerrorhandling()
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        herecouldvebeensomeerrorhandling()
    else:
        f

