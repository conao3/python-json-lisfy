# json-lisfy

A Python tool that converts JSON into S-expression (Lisp-like) syntax.

## Overview

json-lisfy parses JSON input and transforms it into a structured S-expression format, making it suitable for processing with Lisp-based tools or for applications that benefit from a uniform, parenthesized representation of data.

## Installation

```bash
pip install json-lisfy
```

Or with Poetry:

```bash
poetry add json-lisfy
```

## Usage

### Command Line

Run the interactive REPL:

```bash
json-lisfy
```

### Examples

```
json-lisfy> 1
(int nil 1)

json-lisfy> 2.4
(float nil 2.4)

json-lisfy> true
(symbol nil "true")

json-lisfy> null
(symbol nil "null")

json-lisfy> "hello"
(str nil "hello")

json-lisfy> {"a": 1, "b": 2}
(object nil (item nil (str nil "a") (int nil 1)) (item nil (str nil "b") (int nil 2)))

json-lisfy> [1, 2, "text", true]
(array nil (int nil 1) (int nil 2) (str nil "text") (symbol nil "true"))
```

## Output Format

Each JSON value is converted to an S-expression with the following structure:

| JSON Type | S-expression Format |
|-----------|---------------------|
| Integer | `(int nil <value>)` |
| Float | `(float nil <value>)` |
| String | `(str nil "<value>")` |
| Boolean | `(symbol nil "<true\|false>")` |
| Null | `(symbol nil "null")` |
| Array | `(array nil <elements...>)` |
| Object | `(object nil (item nil <key> <value>)...)` |

## Requirements

- Python 3.11+

## License

Apache-2.0
