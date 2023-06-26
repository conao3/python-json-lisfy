from typing import Literal
import typing
import pydantic


## Exceptions

class LisfyError(Exception):
    pass


class ReaderError(LisfyError):
    pass


## Values

class Value(pydantic.BaseModel):
    def lisfy(self, minify: bool=False) -> str:
        raise NotImplementedError


class ValueObject(Value):
    value: dict[str, Value]

    def lisfy(self, minify: bool = False) -> str:
        res = {
            f'"{k}"': v.lisfy(minify=minify)
            for k, v
            in self.value.items()
        }
        return '(' + ' '.join(f'({k} . {v})' for k, v in res.items()) + ')'


class ValueArray(Value):
    value: list[Value]

    def lisfy(self, minify: bool=False) -> str:
        res = [x.lisfy(minify=minify) for x in self.value]
        return '(' + ' '.join(res) + ')'


class ValueString(Value):
    value: str

    def lisfy(self, minify: bool=False) -> str:
        return f'"{self.value}"'


class ValueInteger(Value):
    value: int

    def lisfy(self, minify: bool=False) -> str:
        return str(self.value)


class ValueFloat(Value):
    value: float

    def lisfy(self, minify: bool=False) -> str:
        return str(self.value)


class ValueSymbol(Value):
    value: Literal['EOF', 'null', 'true', 'false']

    def lisfy(self, minify: bool=False) -> str:
        if self.value == 'EOF':
            raise LisfyError('Cannot lisfy EOF')

        if self.value in ('false', 'null'):
            return 'nil'

        if self.value == 'true':
            return 't'

        typing.assert_never(self.value)
