import more_itertools

from . import reader


def read(x: str) -> str:
    stream = more_itertools.peekable(x)
    return reader.read(stream, eof_error_p=False)


def eval(x: str) -> str:
    return x


def print(x: str) -> str:
    return x


def rep(x: str) -> str:
    return print(eval(read(x)))
