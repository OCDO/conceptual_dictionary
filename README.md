# conceptual_dictionary

A Python dictionary template for storing serializable computational-materials-science
metadata. The schema and controlled vocabularies are kept in lock-step with
[atomRDF](https://github.com/pyscal/atomRDF), so YAML/JSON files produced with
`conceptual_dictionary` can be parsed directly by atomRDF's `WorkflowParser`.

- Strongly-typed templates for samples, workflows, properties, operations,
  defects, datasets and math operations.
- Controlled vocabularies mirrored from atomRDF (methods, ensembles, potentials,
  XC functionals, …) with optional runtime validation.
- A `dict` subclass (`ConceptualDict`) with YAML/JSON I/O that automatically
  cleans numpy types and is round-trip safe.

## Installation

```bash
pip install conceptual-dictionary
```

From source:

```bash
pip install -e .
```

## Quick start

```python
import copy
from conceptual_dictionary import (
    ConceptualDict, sample_template, workflow_template,
    property_template, dataset_template,
)

cd = ConceptualDict()

# Sample
sample = copy.deepcopy(sample_template)
sample["id"] = "Al_fcc"
sample["material"]["element_ratio"] = {"Al": 1.0}
sample["material"]["crystal_structure"]["spacegroup_symbol"] = "Fm-3m"
sample["material"]["crystal_structure"]["spacegroup_number"] = 225
sample["material"]["crystal_structure"]["unit_cell"]["lattice_parameter"] = [4.05, 4.05, 4.05]
sample["material"]["crystal_structure"]["unit_cell"]["angle"] = [90.0, 90.0, 90.0]
cd["computational_sample"].append(sample)

# Workflow
wf = copy.deepcopy(workflow_template)
wf["method"] = "MolecularStatics"
wf["interatomic_potential"] = {"potential_type": "eam/alloy",
                               "uri": "https://doi.org/10.1103/physrevb.59.3393"}
wf["input_sample"]  = ["Al_fcc"]
wf["output_sample"] = ["Al_fcc"]

energy = copy.deepcopy(property_template)
energy.update({"label": "EquilibriumEnergy", "value": -3.36, "unit": "EV",
               "associate_to_sample": ["Al_fcc"]})
wf["calculated_property"] = [energy]
cd["workflow"].append(wf)

# Optional dataset provenance
ds = copy.deepcopy(dataset_template)
ds["title"]   = "Al FCC reference"
ds["samples"] = ["Al_fcc"]
cd["dataset"] = ds

cd.validate(strict=True)        # raises on first vocab violation
cd.to_yaml("metadata.yaml")
cd.to_json("metadata.json", indent=2)
```

## Templates

Every template is a plain `dict`. Use `copy.deepcopy` before mutating, then
populate only the fields that apply (everything is optional unless marked
**Required**).

| Import | Purpose |
|---|---|
| `sample_template` | A computational sample (material + simulation cell + atoms) |
| `property_template` | A single calculated/input/output property |
| `workflow_template` | A simulation/calculation step |
| `dataset_template` | DCAT dataset provenance (creators, publication, sample IDs) |
| `operation_template` | Atomic-scale transform (DeleteAtom, Rotate, Translate, Shear, …) |
| `math_operation_template` | Arithmetic activity (Subtraction, Addition, Multiplication, Division, Exponentiation) |
| `vacancy_template`, `substitutional_template`, `interstitial_template` | Point defects |
| `stacking_fault_template` | Stacking fault |
| `grain_boundary_template` | Grain boundary (5 YAML key variants) |
| `dislocation_template` | Dislocation (4 YAML key variants) |
| `defect_complex_template` | Multi-defect complex |
| `full_sample_template`, `full_yaml_template` | Reference templates with **every** supported field |

## `ConceptualDict`

A `dict` subclass pre-populated with the four top-level sections atomRDF reads:

```python
ConceptualDict() == {
    "computational_sample": [],
    "workflow": [],
    "operation": [],
    "math_operation": [],
}
```

Add an optional `"dataset"` key (or anything else) at any time.

### Methods

| Method | Notes |
|---|---|
| `to_yaml(filepath, sort_keys=False)` | numpy → native conversion, preserves insertion order by default |
| `from_yaml(filepath)` *(classmethod)* | Loads any partial YAML (missing top-level keys keep their default empty lists) |
| `to_json(filepath, sort_keys=False, indent=2)` | Same numpy cleanup as YAML |
| `from_json(filepath)` *(classmethod)* | Symmetric counterpart |
| `validate(strict=False)` | Returns a list of violation dicts `{section, index, field, value, allowed}`. With `strict=True` raises `ValueError` on the first violation |
| `generate_id(length=7)` | Collision-resistant random ID using `os.urandom` (safe against third-party `random.seed()`) |

### Numpy-friendly serialization

Both `to_yaml` and `to_json` recursively convert `np.ndarray`, `np.floating`,
`np.integer`, `np.bool_` and any unknown object (via `str(obj)`) to JSON/YAML
native types — so values coming from ASE / pyiron / LAMMPS need no
pre-processing.

## File layout produced

The full top-level YAML/JSON shape consumed by atomRDF:

```yaml
dataset:                  # optional, dcat:Dataset provenance
  identifier: ...
  title: ...
  creators: [{id, name}, ...]
  publication: {id, identifier, title}
  samples: [<sample id>, ...]

computational_sample:     # list of sample dicts
  - id: ...
    material: {...}
    simulation_cell: {...}
    atom_attribute: {...}
    calculated_property: [...]
    # optional defect blocks (see Defects below)

workflow:                 # list of workflow steps
  - method: ...
    algorithm: ...
    ...

operation:                # list of atomic-scale transforms (legacy alias: 'activity')
  - method: ...
    input_sample: ...
    output_sample: ...

math_operation:           # list of arithmetic activities
  - type: ...
    result: {...}
```

## Controlled vocabularies (cross-referenced with atomRDF)

The following sections enumerate **every string atomRDF accepts** for each
field. Aliases are marked → canonical. Anything outside these sets is rejected
by `ConceptualDict.validate()` (and silently ignored or errored by atomRDF
depending on the field).

The frozen sets are also importable and useful for building UIs:

```python
from conceptual_dictionary import (
    METHOD, ALGORITHM, DEGREES_OF_FREEDOM, THERMODYNAMIC_ENSEMBLE,
    POTENTIAL_TYPE, XC_FUNCTIONAL, OPERATION_METHOD,
    MATH_OPERATION_TYPE, GRAIN_BOUNDARY_TYPE, YAML_TOP_LEVEL_KEYS,
    CONTROLLED_VALUES,
)
```

### Workflow

| Field | Accepted values | atomRDF source |
|---|---|---|
| `workflow.method` | `MolecularDynamics`, `MolecularStatics`, `DensityFunctionalTheory` | `atomrdf/datamodels/workflow/method.py` (`method_map`) |
| `workflow.algorithm` | `EquationOfStateFit`, `QuasiHarmonicApproximation`, `ThermodynamicIntegration`, `ANNNIModel`, `TensileTest`, `CompressionTest`; alias `UniaxialTension` → `TensileTest` | `atomrdf/datamodels/workflow/algorithm.py` (`algorithm_map`) |
| `workflow.degrees_of_freedom` *(list)* | `AtomicPositionRelaxation`, `CellVolumeRelaxation`, `CellShapeRelaxation` | `atomrdf/datamodels/workflow/dof.py` (`dof_map`) |
| `workflow.thermodynamic_ensemble` | `CanonicalEnsemble` (NVT), `MicrocanonicalEnsemble` (NVE), `IsothermalIsobaricEnsemble` (NPT), `IsoenthalpicIsobaricEnsemble` (NPH), `GrandCanonicalEnsemble` (μVT) | `atomrdf/datamodels/workflow/ensemble.py` (`ensemble_map`) |
| `workflow.xc_functional` | `LDA`, `GGA`, `PBE` (→ GGA), `LocalDensityApproximation`, `GeneralizedGradientApproximation`, `PerdewBurkeErnzerhof` (→ GGA), `HybridFunctional`, `HybridGeneralizedGradientApproximation`, `HybridMetaGeneralizedGradientApproximation`, `MetaGeneralizedGradientApproximation` | `atomrdf/datamodels/workflow/xcfunctional.py` (`xc_map`) |

### Interatomic potential type

`workflow.interatomic_potential.potential_type` accepts the canonical class
name **or** any short alias atomRDF understands:

| Family | Canonical | Aliases |
|---|---|---|
| Generic | `InteratomicPotential` | — |
| EAM | `EmbeddedAtomModel` | `EAM`, `eam`, `eam/alloy`, `eam/fs` |
| MEAM | `ModifiedEmbeddedAtomModel` | `MEAM`, `meam` |
| Lennard–Jones | `LennardJonesPotential` | `LJ`, `lj` |
| Machine learning | `MachineLearningPotential` | `ACE`, `pace`, `HDNNP`, `hdnnp`, `GRACE`, `grace` |

Source: `atomrdf/datamodels/workflow/potential.py` (`potential_map`).

### Operation methods

`operation.method` (legacy top-level key `activity` is also accepted):

`DeleteAtom`, `SubstituteAtom`, `AddAtom`, `Rotate` (alias `Rotation`),
`Translate` (alias `Translation`), `Shear`.

Source: `atomrdf/io/workflow_parser.py` (`OPERATION_MAP`).

### Math operations

`math_operation.type`: `Subtraction`, `Addition`, `Multiplication`, `Division`,
`Exponentiation`. Operands are either a scalar **or** a property `id` string
referencing a previously declared `calculated_property` / `input_parameter` /
`output_parameter`:

| `type` | Operand fields |
|---|---|
| `Subtraction` | `minuend`, `subtrahend` |
| `Addition` | `addend` *(list)* |
| `Multiplication` | `factor` *(list)* |
| `Division` | `dividend`, `divisor` |
| `Exponentiation` | `base`, `exponent` |

Source: `atomrdf/datamodels/workflow/math_operations.py`.

### Property `label` / `basename`

`label` and `basename` on a property are **not validated** as a closed enum,
but at RDF generation time atomRDF resolves `basename` against the
[ASMO](https://github.com/Materials-Data-Science-and-Informatics/asmo)
ontology via `getattr(ASMO, basename)`, so the value should match an ASMO
class. The following terms appear in atomRDF's source / parsers / visualizer
and are known to round-trip correctly:

| Category | Recognised terms |
|---|---|
| Energies | `TotalEnergy`, `Energy`, `EquilibriumEnergy`, `CohesiveEnergy`, `FormationEnergy`, `VacancyFormationEnergy`, `GrainBoundaryEnergy`, `SurfaceEnergy`, `StackingFaultEnergy`, `SegregationEnergy`, `WorkOfSeparation`, `MigrationEnergy` |
| Mechanical | `BulkModulus`, `ElasticConstant`, `C11`, `C12`, `C44`, `Stress`, `Pressure` |
| Geometric | `Volume`, `EquilibriumVolume`, `LatticeConstant` |
| Thermo / state | `Temperature` |
| Generic wrappers | `CalculatedProperty`, `Property`, `AtomAttribute` |

Custom strings outside this list will still be written to the YAML/JSON
verbatim — they just won't resolve to a known ASMO class when loaded into an
RDF graph. Sources: `atomrdf/datamodels/workflow/property.py`,
`atomrdf/visualize.py`, `atomrdf/io/reconstruct.py`,
`atomrdf/parsers/pyiron.py`.

### Property `unit`

The unit string is suffixed onto `http://qudt.org/vocab/unit/{unit}` and
stored as a [QUDT](https://www.qudt.org/) URI — there is **no closed enum**
in atomRDF, so any valid QUDT unit code is accepted. Examples that appear in
atomRDF or its examples:

| Quantity | Common QUDT codes |
|---|---|
| Energy | `EV`, `J`, `KiloCAL` |
| Length | `ANGSTROM`, `M`, `NanoM` |
| Volume | `ANGSTROM3`, `M3` |
| Temperature | `K`, `DEG_C` |
| Pressure / stress | `PA`, `GigaPA`, `BAR` |
| Force | `N`, `EV-PER-ANGSTROM` |
| Angle | `RAD`, `DEG` |

Source: `atomrdf/datamodels/workflow/property.py` line 93.

### Defects (sample-level YAML keys)

Place at most one of these as a key inside a sample dict.

| Family | YAML keys | Template | Fields |
|---|---|---|---|
| Point defect | `vacancy`, `substitutional`, `interstitial` | `vacancy_template`, `substitutional_template`, `interstitial_template` | `concentration` (atomic fraction), `number` |
| Stacking fault | `stacking_fault` | `stacking_fault_template` | `plane` (Miller indices), `displacement` (3-vector) |
| Grain boundary | `grain_boundary`, `tilt_grain_boundary`, `twist_grain_boundary`, `symmetric_tilt_grain_boundary`, `mixed_grain_boundary` | `grain_boundary_template` | `sigma`, `plane`, `misorientation_angle`, `rotation_axis` |
| Dislocation | `dislocation`, `edge_dislocation`, `screw_dislocation`, `mixed_dislocation` | `dislocation_template` | `line_direction`, `burgers_vector`, `slip_system.{slip_direction, slip_plane.normal}`, plus `character_angle` for `mixed_dislocation` |
| Defect complex | `defect_complex` | `defect_complex_template` | `ids` (list of defect key names), `relative_distance` |

Source: `atomrdf/datamodels/structure.py`,
`atomrdf/datamodels/defects/{pointdefects,grainboundary,dislocation,stackingfault,complex}.py`.

The frozen set `GRAIN_BOUNDARY_TYPE` enumerates the five GB key variants.

### Material / crystal structure

| Field | Notes |
|---|---|
| `material.element_ratio` | `{symbol: fraction}`, e.g. `{"Fe": 0.8, "Cr": 0.2}` |
| `material.crystal_structure.spacegroup_symbol` | Hermann–Mauguin (e.g. `"Fm-3m"`) — **no validation** |
| `material.crystal_structure.spacegroup_number` | 1–230 — **no validation** |
| `material.crystal_structure.unit_cell.bravais_lattice` | URI string. Common values used in atomRDF: `https://www.wikidata.org/wiki/Q851536` (bcc), `Q3006714` (fcc), `Q663314` (hcp), `Q2242450` (sc), `Q503601` (tetragonal), `Q648961` (orthorhombic), `Q624543` (monoclinic), `Q13362463` (rhombohedral) |
| `material.crystal_structure.unit_cell.lattice_parameter` | `[a, b, c]` in Å |
| `material.crystal_structure.unit_cell.angle` | `[α, β, γ]` in degrees |

### Atom attribute

| Field | Notes |
|---|---|
| `position` | List of `[x, y, z]` (Å) — for inline small systems |
| `species` | List of element symbols, parallel to `position` |
| `file_path` | Path to a structure file (resolved relative to the YAML file). Preferred for large MD snapshots |
| `file_format` | ASE format string (e.g. `"lammps-data"`, `"lammps-dump-text"`, `"vasp"`, `"aims"`); auto-detected when `None` |
| `file_species` | Species order for LAMMPS numeric atom types (e.g. `["Al"]`) |

Source: `atomrdf/io/workflow_parser.py` `_resolve_atom_attribute_from_file`.

### Software / workflow manager

```yaml
software:
  - uri: https://doi.org/10.1016/j.cpc.2021.108171
    label: LAMMPS
    version: "29Sep2021"
workflow_manager:
  uri: ...
  label: ...
  version: ...
```

Source: `atomrdf/datamodels/workflow/software.py`.

### Top-level keys

`YAML_TOP_LEVEL_KEYS = {computational_sample, workflow, operation, activity (legacy), math_operation}`.
Plus `dataset` (DCAT provenance, parsed by atomRDF if present).

## Cross-referencing properties in `math_operation`

A property may carry an `id`; later math operations reference it by string:

```python
e_def = copy.deepcopy(property_template)
e_def.update({"id": "E_def", "label": "TotalEnergy", "value": -3.20, "unit": "EV"})

e_perf = copy.deepcopy(property_template)
e_perf.update({"id": "E_perf", "label": "TotalEnergy", "value": -3.36, "unit": "EV"})

cd["workflow"][0]["calculated_property"] = [e_def, e_perf]
cd["math_operation"].append({
    "type": "Subtraction",
    "minuend": "E_def",
    "subtrahend": "E_perf",
    "result": {"id": "E_form", "label": "FormationEnergy", "unit": "EV",
               "associate_to_sample": ["Al_fcc_with_vacancy"]},
})
```

## Validation

```python
violations = cd.validate()           # warns on each violation, returns the list
cd.validate(strict=True)             # raises ValueError on the first violation
```

`validate()` currently checks `workflow.method`, `workflow.algorithm`,
`workflow.degrees_of_freedom`, `workflow.thermodynamic_ensemble`,
`workflow.xc_functional`, `workflow.interatomic_potential.potential_type`,
`operation.method` and `math_operation.type`. Each violation dict has keys
`section`, `index`, `field`, `value`, `allowed`.

## Examples

Working YAML/JSON examples live in [`examples/`](examples/):

- `single_structure_with_workflow.yaml` / `.json`
- `grain_boundary.yaml` / `.json`
- `examples.ipynb` — end-to-end notebook

## Citation

If you use `conceptual_dictionary` in your research, please cite the
associated paper:

> A. Azocar Guzman, S. Menon, T. Hickel, S. Sandfeld.
> *Ontology-based knowledge graph infrastructure for interoperable atomistic
> simulation data.* arXiv:2604.06230 (2026).
> <https://arxiv.org/abs/2604.06230>

BibTeX:

```bibtex
@misc{guzman2026ontologybasedknowledgegraphinfrastructure,
      title={Ontology-based knowledge graph infrastructure for interoperable atomistic simulation data},
      author={Abril Azocar Guzman and Sarath Menon and Tilmann Hickel and Stefan Sandfeld},
      year={2026},
      eprint={2604.06230},
      archivePrefix={arXiv},
      primaryClass={cs.DB},
      url={https://arxiv.org/abs/2604.06230},
}
```

## License

MIT License — see [LICENSE](LICENSE).
