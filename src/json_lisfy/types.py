import pydantic


class Value(pydantic.BaseModel):
    pass


class ValueObject(Value):
    value: dict[str, Value]


class ValueArray(Value):
    value: list[Value]


class ValueString(Value):
    value: str


class ValueInteger(Value):
    value: int


class ValueFloat(Value):
    value: float


class ValueSymbol(Value):
    value: str
