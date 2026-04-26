import sys


def herecouldvebeensomeerrorhandling() -> None:
    exit()


def handle_input() -> None:
    if len(sys.argv) != 2:
        herecouldvebeensomeerrorhandling()
    try:
        f = open(sys.argv[1], "r")
    except IOError:
        herecouldvebeensomeerrorhandling()

