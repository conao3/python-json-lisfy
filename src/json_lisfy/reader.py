from __future__ import annotations
from typing import Optional

import more_itertools

from . import types
from . import subr


def read_string(input_stream: more_itertools.peekable[str]) -> types.ValueString:
    next(input_stream)  # Skip the opening '"'.
    value = ''

    while True:
        peek = input_stream.peek(None)

        if peek is None:
            raise types.ReaderError('Unexpected EOF')

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

    i, _ = subr.subr.trap(lambda: int(value))
    if i is not None:
        return types.ValueInteger(value=i)

    f, _ = subr.subr.trap(lambda: float(value))
    if f is not None:
        return types.ValueFloat(value=f)

    raise types.ReaderError(f'Could not parse as a number: {value}')


def read_symbol(input_stream: more_itertools.peekable[str]) -> types.ValueSymbol:
    peek = input_stream.peek(None)

    if peek is None:
        raise types.ReaderError('Unexpected EOF')

    if peek.lower() == 't':
        s = ''.join(more_itertools.take(4, input_stream))
        if s.lower() != 'true':
            raise types.ReaderError(f'Unexpected chars: {s}')
        return types.ValueSymbol(value='true')

    if peek.lower() == 'f':
        s = ''.join(more_itertools.take(5, input_stream))
        if s.lower() != 'false':
            raise types.ReaderError(f'Unexpected chars: {s}')
        return types.ValueSymbol(value='false')

    if peek.lower() == 'n':
        s = ''.join(more_itertools.take(4, input_stream))
        if s.lower() != 'null':
            raise types.ReaderError(f'Unexpected chars: {s}')
        return types.ValueSymbol(value='null')

    raise types.ReaderError(f'Unexpected char: {peek}')


def read_object(input_stream: more_itertools.peekable[str]) -> types.ValueObject:
    next(input_stream)  # Skip the opening '{'.

    subr.reader.skip_whitespace(input_stream)
    peek = input_stream.peek(None)

    if peek == '}':
        next(input_stream)  # Skip the closing '}'.
        return types.ValueObject(value={})

    value = {}

    while True:
        key = read(input_stream, recursive_p=True)

        subr.reader.skip_whitespace_and_ensure(input_stream, ':')
        value[key] = read(input_stream, recursive_p=True)

        subr.reader.skip_whitespace(input_stream)
        peek = input_stream.peek(None)
        if peek is None:
            raise types.ReaderError('Unexpected EOF')

        if peek == '}':
            break

        if peek != ',':
            raise types.ReaderError(f'Expected a comma or closing brace, but got: {peek}')

        next(input_stream)  # Skip the comma.

    next(input_stream)  # Skip the closing '}'.
    return types.ValueObject(value=value)


def read_array(input_stream: more_itertools.peekable[str]) -> types.ValueArray:
    next(input_stream)  # Skip the opening '['.

    subr.reader.skip_whitespace(input_stream)
    peek = input_stream.peek(None)

    if peek == ']':
        next(input_stream)  # Skip the closing ']'.
        return types.ValueArray(value=[])

    value: list[types.Value] = []

    while True:
        value.append(read(input_stream, recursive_p=True))

        subr.reader.skip_whitespace(input_stream)
        peek = input_stream.peek(None)
        if peek is None:
            raise types.ReaderError('Unexpected EOF')

        if peek == ']':
            break

        if peek != ',':
            raise types.ReaderError(f'Expected a comma or closing bracket, but got: {peek}')

        next(input_stream)  # Skip the comma.

    next(input_stream)  # Skip the closing ']'.
    return types.ValueArray(value=value)


def read(
    input_stream: more_itertools.peekable[str],
    eof_error_p: bool = True,
    eof_value: Optional[types.Value] = None,
    recursive_p: bool = False,
) -> types.Value:
    peek = subr.reader.peek_char(True, input_stream, False, 'EOF', recursive_p)

    if peek == 'EOF':
        if eof_error_p:
            raise types.ReaderError('Unexpected EOF')

        if eof_value is None:
            raise ValueError('eof_value must be provided if eof_error_p is False')

        return eof_value

    if peek == '{':
        return read_object(input_stream)

    if peek == '}':
        raise types.ReaderError('Unexpected }')

    if peek == '[':
        return read_array(input_stream)

    if peek == ']':
        raise types.ReaderError('Unexpected ]')

    if peek == '"':
        return read_string(input_stream)

    if peek in '0123456789-+':
        return read_number(input_stream)

    return read_symbol(input_stream)
