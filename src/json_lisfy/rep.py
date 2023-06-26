from typing import Optional
import more_itertools

from . import reader
from . import types


def read(x: str) -> Optional[types.Value]:
    stream = more_itertools.peekable(x)
    return reader.read(stream, eof_error_p=False)


def eval(x: Optional[types.Value]) -> Optional[types.Value]:
    return x


def print(x: Optional[types.Value]) -> Optional[str]:
    return str(x)


def rep(x: str) -> Optional[str]:
    return print(eval(read(x)))
