# Templates

Every template is a plain `dict`. Use `copy.deepcopy` before mutating
anything nested, then populate only the fields that apply (everything is
optional unless marked **Required**).

```python
import copy
from conceptual_dictionary import sample_template

s = copy.deepcopy(sample_template)
s["id"] = "Al_fcc"
```

## Available templates

| Import | Purpose |
| ------ | ------- |
| `sample_template` | A computational sample (material + simulation cell + atoms) |
| `property_template` | A single calculated / input / output property |
| `workflow_template` | A simulation / calculation step |
| `dataset_template` | DCAT dataset provenance (creators, publication, sample IDs) |
| `operation_template` | Atomic-scale transform (DeleteAtom, Rotate, Translate, Shear, …) |
| `math_operation_template` | Arithmetic activity (Subtraction, Addition, Multiplication, Division, Exponentiation) |
| `vacancy_template`, `substitutional_template`, `interstitial_template` | Point defects |
| `stacking_fault_template` | Stacking fault |
| `grain_boundary_template` | Grain boundary (5 YAML key variants) |
| `dislocation_template` | Dislocation (4 YAML key variants) |
| `defect_complex_template` | Multi-defect complex |
| `full_sample_template`, `full_yaml_template` | Reference templates with **every** supported field |

All templates are importable both from the top-level package
(`from conceptual_dictionary import sample_template`) and from
`conceptual_dictionary.templates`.

---

## `sample_template`

```python
{
    "id": "sample1",
    "material": {
        "element_ratio": {},
        "crystal_structure": {
            "spacegroup_symbol": None,
            "spacegroup_number": None,
            "unit_cell": {
                "bravais_lattice": None,
                "lattice_parameter": None,
                "angle": [],
            },
        },
    },
    "simulation_cell": {
        "volume": {"value": None},
        "number_of_atoms": None,
        "length": [],
        "vector": [],
        "angle": [],
        "repetitions": [],
        "grain_size": None,
        "number_of_grains": 0,
    },
    "atom_attribute": {
        "position": None,            # inline arrays
        "species": None,
        "file_path": None,           # OR file reference (preferred for big systems)
        "file_format": None,         # ASE format string
        "file_species": None,        # species order for LAMMPS numeric types
    },
    "calculated_property": [],
}
```

### Defect blocks

A sample may carry **at most one** defect block per category, simply by adding
the appropriate top-level key inside the sample dict. atomRDF recognises:

| Category | YAML keys | Template |
| -------- | --------- | -------- |
| Point defect | `vacancy`, `substitutional`, `interstitial` | `vacancy_template`, `substitutional_template`, `interstitial_template` |
| Stacking fault | `stacking_fault` | `stacking_fault_template` |
| Grain boundary | `grain_boundary`, `tilt_grain_boundary`, `twist_grain_boundary`, `symmetric_tilt_grain_boundary`, `mixed_grain_boundary` | `grain_boundary_template` |
| Dislocation | `dislocation`, `edge_dislocation`, `screw_dislocation`, `mixed_dislocation` | `dislocation_template` |
| Defect complex | `defect_complex` | `defect_complex_template` |

For example, to mark the sample as containing a vacancy:

```python
sample["vacancy"] = {"concentration": 0.004, "number": 1}
```

`mixed_dislocation` additionally accepts a `character_angle` field (degrees).

---

## `property_template`

```python
{
    "id": None,                   # optional local ID; referenced by math_operation operands
    "label": None,                # primary name; resolved against ASMO classes by atomRDF
    "basename": None,             # legacy alias of label (kept for backwards compat)
    "value": None,
    "unit": None,                 # QUDT code (e.g. "EV", "ANGSTROM3")
    "associate_to_sample": [],    # list of sample IDs this property belongs to
}
```

See [](vocabularies.md#property-label-basename) for the list of `label` values
atomRDF rounds-trips and the QUDT unit conventions.

---

## `workflow_template`

```python
{
    "algorithm": None,                  # see vocabularies.md
    "method": None,                     # see vocabularies.md
    "xc_functional": None,              # DFT only
    "input_parameter": [],              # list of property dicts
    "input_sample": [],                 # list of sample ids
    "output_sample": [],                # list of sample ids
    "output_parameter": [],
    "calculated_property": [],
    "degrees_of_freedom": [],           # list of dof strings
    "interatomic_potential": {
        "potential_type": None,
        "uri": None,
    },
    "software": [],                     # list of {uri, version, label}
    "workflow_manager": {"uri": None, "version": None, "label": None},
    "thermodynamic_ensemble": None,
}
```

---

## `dataset_template`

DCAT-style dataset provenance:

```python
{
    "identifier": None,               # dataset URI / DOI
    "title": None,
    "creators": [{"id": None, "name": None}],   # foaf:Person entries
    "publication": {                            # dcterms:isReferencedBy
        "id": None,
        "identifier": None,                     # DOI string
        "title": None,
    },
    "samples": [],                              # sample IDs in the dataset
}
```

---

## `operation_template`

Atomic-scale transform operations have a unified template containing every
possible field; populate only what applies for your `method`:

```python
{
    "method": None,                # Required — see vocabularies.md
    "input_sample": None,          # Required
    "output_sample": None,         # Required
    "rotation_matrix": None,       # Rotate
    "translation_vector": None,    # Translate
    "shear_vector": None,          # Shear
    "normal_vector": None,         # Shear (optional)
    "distance": None,              # Shear (optional)
}
```

---

## `math_operation_template`

ASMO arithmetic activity. Operands are either a numeric scalar **or** a
property `id` string referencing a previously declared `calculated_property` /
`input_parameter` / `output_parameter`. The result is itself a property and may
carry its own `id` so later math operations can use it as an operand.

```python
{
    "type": None,                    # Required: Subtraction | Addition | Multiplication | Division | Exponentiation
    "result": {
        "id": None,
        "label": None,
        "basename": None,
        "value": None,
        "unit": None,
        "associate_to_sample": [],
    },
    # Subtraction
    "minuend": None,
    "subtrahend": None,
    # Addition
    "addend": [],
    # Multiplication
    "factor": [],
    # Division
    "dividend": None,
    "divisor": None,
    # Exponentiation
    "base": None,
    "exponent": None,
}
```

Example — vacancy formation energy as `E_def − E_perf`:

```python
import copy
from conceptual_dictionary import property_template

e_def  = copy.deepcopy(property_template); e_def.update({
    "id": "E_def",  "label": "TotalEnergy", "value": -3.20, "unit": "EV"})
e_perf = copy.deepcopy(property_template); e_perf.update({
    "id": "E_perf", "label": "TotalEnergy", "value": -3.36, "unit": "EV"})

cd["workflow"][0]["calculated_property"] = [e_def, e_perf]

cd["math_operation"].append({
    "type": "Subtraction",
    "minuend": "E_def",
    "subtrahend": "E_perf",
    "result": {
        "id": "E_form", "label": "FormationEnergy",
        "unit": "EV", "associate_to_sample": ["Al_fcc_with_vacancy"],
    },
})
```

---

## `full_sample_template` / `full_yaml_template`

These mirror the full nested shape with every supported key in the correct
position — useful as a copy-and-trim schema reference. See the source in
`conceptual_dictionary/templates/full.py` or import them:

```python
from conceptual_dictionary import full_sample_template, full_yaml_template
```
