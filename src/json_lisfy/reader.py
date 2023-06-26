from __future__ import annotations

import more_itertools

from . import types
from . import subr


def skip_whitespace(input_stream: more_itertools.peekable[str]) -> None:
    while (peek := input_stream.peek(None)) and peek.isspace():
        next(input_stream)


def read_string(input_stream: more_itertools.peekable[str]) -> types.ValueString:
    next(input_stream)  # Skip the opening '"'.
    value = ''

    while True:
        peek = input_stream.peek(None)

        if peek is None:
            raise EOFError('Unexpected EOF')

        if peek == '"':
            break

        value += peek
        next(input_stream)

    next(input_stream)  # Skip the closing '"'.
    return types.ValueString(value=value)


def read_number(input_stream: more_itertools.peekable[str]) -> types.ValueInteger | types.ValueFloat:
    value = ''

    while (peek := input_stream.peek(None)) and peek in '0123456789-+.eE':
        value += peek
        next(input_stream)

    i, _ = subr.trap(lambda: int(value))
    if i is not None:
        return types.ValueInteger(value=i)

    f, _ = subr.trap(lambda: float(value))
    if f is not None:
        return types.ValueFloat(value=f)

    raise types.ReaderError(f'Could not parse as a number: {value}')


def read(
    input_stream: more_itertools.peekable[str],
    eof_error_p: bool = True,
    eof_value: types.Value = types.ValueSymbol(value='EOF'),
    recursive_p: bool = False,
) -> types.Value:
    skip_whitespace(input_stream)

    peek = input_stream.peek(None)

    if peek is None:
        if eof_error_p:
            raise EOFError('Unexpected EOF')
        return eof_value

    if peek == '"':
        return read_string(input_stream)

    if peek in '0123456789-+':
        return read_number(input_stream)

    return types.ValueSymbol(value='EOF')
