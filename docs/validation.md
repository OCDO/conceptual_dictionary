# Validation

`ConceptualDict.validate` checks the controlled-vocabulary fields against
[`vocabs.CONTROLLED_VALUES`](vocabularies.md). It is **opt-in** — atomRDF will
itself flag many issues at parse time, but running validation early gives you
fast, file-local feedback before any RDF graph is built.

## Modes

```python
warnings = cd.validate(strict=False)   # default — returns list[str]; never raises
cd.validate(strict=True)               # raises ValueError on first violation
```

In non-strict mode the return value is a list of human-readable strings, one
per violation. An empty list means the document is clean.

## What is checked

For every entry in the corresponding section, the following fields are
compared against the frozen sets in `vocabs`:

| Field path | Vocabulary |
| ---------- | ---------- |
| `workflow[*].method` | `vocabs.METHOD` |
| `workflow[*].algorithm` | `vocabs.ALGORITHM` |
| `workflow[*].degrees_of_freedom[*]` | `vocabs.DEGREES_OF_FREEDOM` |
| `workflow[*].thermodynamic_ensemble` | `vocabs.THERMODYNAMIC_ENSEMBLE` |
| `workflow[*].xc_functional` | `vocabs.XC_FUNCTIONAL` |
| `workflow[*].interatomic_potential.potential_type` | `vocabs.POTENTIAL_TYPE` |
| `operation[*].method` | `vocabs.OPERATION_METHOD` |
| `math_operation[*].type` | `vocabs.MATH_OPERATION_TYPE` |

Both `operation` and the legacy alias `activity` are walked.

## What is **not** checked

- Property `label` / `basename` (open vocabulary — atomRDF stores unknown
  labels verbatim)
- `unit` (open QUDT enumeration)
- Cross-references between `id` strings (e.g. that a `math_operation`'s
  `minuend` resolves to a known property `id`) — atomRDF reports these at
  parse time
- Required-field presence (build via the templates and the shape is correct
  by construction)

## Example

```python
from conceptual_dictionary import ConceptualDict, workflow_template
import copy

cd = ConceptualDict()
wf = copy.deepcopy(workflow_template)
wf["method"] = "DFT"          # typo: should be "DensityFunctionalTheory"
cd["workflow"].append(wf)

cd.validate()
# → ['workflow[0].method: "DFT" not in vocabulary {...}']

cd.validate(strict=True)
# → ValueError: workflow[0].method: "DFT" not in vocabulary {...}
```
