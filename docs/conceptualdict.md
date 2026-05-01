# `ConceptualDict`

`ConceptualDict` is a `dict` subclass pre-populated with the four top-level
sections atomRDF's `WorkflowParser` reads:

```python
ConceptualDict() == {
    "computational_sample": [],
    "workflow": [],
    "operation": [],
    "math_operation": [],
}
```

Arbitrary additional top-level keys (e.g. `"dataset"`) may be added at any
time via normal item assignment. All standard `dict` methods (`update`, `get`,
`setdefault`, iteration, …) are inherited.

## Construction

```python
from conceptual_dictionary import ConceptualDict

cd = ConceptualDict()                                  # default empty sections

cd2 = ConceptualDict({"computational_sample": [...]})  # merge a mapping
                                                       # on top of the defaults
```

## I/O

| Method | Notes |
| ------ | ----- |
| `to_yaml(filepath, sort_keys=False)` | numpy → native conversion, preserves insertion order by default |
| `from_yaml(filepath)` *(classmethod)* | Loads any partial YAML (missing top-level keys keep their default empty lists) |
| `to_json(filepath, sort_keys=False, indent=2)` | Same numpy cleanup as YAML |
| `from_json(filepath)` *(classmethod)* | Symmetric counterpart |

```python
cd.to_yaml("out.yaml")
cd.to_json("out.json", indent=2)

cd_loaded = ConceptualDict.from_yaml("out.yaml")
```

### Numpy-friendly serialisation

Both `to_yaml` and `to_json` recursively convert `np.ndarray`, `np.floating`,
`np.integer`, `np.bool_` and any unknown object (via `str(obj)`) to native
Python types — so values coming straight out of ASE / pyiron / LAMMPS can be
stored without manual cleanup:

```python
import numpy as np
cd["computational_sample"][0]["atom_attribute"]["position"] = np.zeros((4, 3))
cd.to_yaml("out.yaml")     # arrays are serialised as nested lists
```

## `validate`

See the dedicated [validation page](validation.md).

## `generate_id`

```python
cd.generate_id()           # 7-character alphanumeric, e.g. "g7K9pXq"
cd.generate_id(length=12)  # custom length
```

Uses `os.urandom`, **not** Python's `random` module — so third-party libraries
that call `random.seed()` (e.g. PyIron / LAMMPS wrappers) cannot make IDs
deterministic across iterations.
