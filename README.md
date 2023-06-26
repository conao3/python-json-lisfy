# python-json-lisfy

## Usage

```bash
$ poetry install
$ poetry run json-lisfy
```

## Example

```bash
$ poetry run json-lisfy
json-lisfy> {"a": 1, "b": 2}
((a . 1) (b . 2))

json-lisfy> [ 1, 2,    "asdf"  , true, false, null]
(1 2.4 "asdf" t nil nil)
```

## Warning

Lisfy is CommonLisp based, so it is not represent difference `false` and `null`.

```bash
json-lisfy> {"asdf": true}
(("asdf" . t))

json-lisfy> {"asdf": false}
(("asdf" . nil))

json-lisfy> {"asdf": null}
(("asdf" . nil))
```
