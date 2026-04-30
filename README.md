# conceptual_dictionary

A Python dictionary template for storing serializable computational-materials-science
metadata. The schema and controlled vocabularies are kept in sync with
[atomRDF](https://github.com/pyscal/atomRDF), so YAML/JSON files produced with
`conceptual_dictionary` can be parsed directly by atomRDF's `WorkflowParser`.

## Installation

From PyPI:

```bash
pip install conceptual-dictionary
```

From source:

```bash
pip install -e .
```

## Usage

### Templates

Every template is a plain `dict`. Copy it (use `copy.deepcopy` for nested
templates) and fill in the fields that apply:

```python
import copy
from conceptual_dictionary import sample_template, workflow_template

sample = copy.deepcopy(sample_template)
sample["id"] = "Al_fcc"
sample["material"]["element_ratio"] = {"Al": 1.0}
sample["simulation_cell"]["volume"]["value"] = 1000

wf = copy.deepcopy(workflow_template)
wf["method"] = "MolecularDynamics"
wf["thermodynamic_ensemble"] = "CanonicalEnsemble"
wf["interatomic_potential"]["potential_type"] = "EAM"
```

Available templates (all importable from `conceptual_dictionary`):

| Template | Purpose |
|---|---|
| `sample_template` | A computational sample (material + simulation cell + atoms) |
| `property_template` | A single calculated/input/output property |
| `workflow_template` | A simulation/calculation step |
| `dataset_template` | DCAT dataset provenance (creators, publication, sample IDs) |
| `operation_template` | Atomic-scale transform (DeleteAtom, Rotate, Translate, Shear, ...) |
| `math_operation_template` | Arithmetic activity (Subtraction, Addition, ...) |
| `vacancy_template`, `substitutional_template`, `interstitial_template` | Point defects |
| `stacking_fault_template` | Stacking fault |
| `grain_boundary_template` | Grain boundary (5 YAML key variants) |
| `dislocation_template` | Dislocation (4 YAML key variants) |
| `defect_complex_template` | Multi-defect complex |
| `full_sample_template`, `full_yaml_template` | Reference templates with every supported field |

### `ConceptualDict`

`ConceptualDict` is a `dict` subclass pre-populated with the top-level sections
that atomRDF's `WorkflowParser` consumes (`computational_sample`, `workflow`,
`operation`, `math_operation`). Use ordinary dict access to populate it, then
serialize:

```python
import copy
from conceptual_dictionary import ConceptualDict, sample_template, workflow_template

cd = ConceptualDict()

# Add a sample
sample = copy.deepcopy(sample_template)
sample["id"] = "Al_fcc"
sample["material"]["element_ratio"] = {"Al": 1.0}
cd["computational_sample"].append(sample)

# Add a workflow step
wf = copy.deepcopy(workflow_template)
wf["method"] = "MolecularDynamics"
wf["input_sample"] = ["Al_fcc"]
cd["workflow"].append(wf)

# Serialize
cd.to_yaml("metadata.yaml")
cd.to_json("metadata.json", indent=2)

# Load back
cd2 = ConceptualDict.from_yaml("metadata.yaml")
cd3 = ConceptualDict.from_json("metadata.json")
```

`ConceptualDict.generate_id(length=7)` returns a collision-resistant random
alphanumeric ID (uses `os.urandom`, safe against third-party `random.seed()`
calls).

### Validation

`ConceptualDict.validate()` checks every entry against the controlled
vocabularies mirrored from atomRDF (methods, algorithms, ensembles, potential
types, XC functionals, operation methods, math-operation types):

```python
violations = cd.validate()           # warns on each violation, returns the list
cd.validate(strict=True)             # raises ValueError on the first violation
```

Each violation is a dict with keys `section`, `index`, `field`, `value`,
`allowed`.

### Controlled vocabularies

The full set is available as frozen sets, useful for building UIs or custom
validators:

```python
from conceptual_dictionary import (
    METHOD, ALGORITHM, DEGREES_OF_FREEDOM, THERMODYNAMIC_ENSEMBLE,
    POTENTIAL_TYPE, XC_FUNCTIONAL, OPERATION_METHOD,
    MATH_OPERATION_TYPE, GRAIN_BOUNDARY_TYPE, YAML_TOP_LEVEL_KEYS,
    CONTROLLED_VALUES,
)
```

## Examples

Working YAML/JSON examples live in [`examples/`](examples/):

- `single_structure_with_workflow.yaml` / `.json`
- `grain_boundary.yaml` / `.json`
- `examples.ipynb` — end-to-end notebook

## License

MIT License — see [LICENSE](LICENSE).
