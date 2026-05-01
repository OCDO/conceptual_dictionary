# Vocabularies

`conceptual_dictionary.vocabs` mirrors the controlled vocabularies that
[atomRDF](https://github.com/pyscal/atomRDF) accepts. Every set below is also
exposed via the lookup dictionary `CONTROLLED_VALUES` used by
[`ConceptualDict.validate`](validation.md).

```python
from conceptual_dictionary import vocabs
sorted(vocabs.METHOD)           # frozenset
vocabs.CONTROLLED_VALUES        # field_path → (frozenset, human-readable scope)
```

## Top-level YAML keys

| Key | Notes |
| --- | ----- |
| `computational_sample` | List of sample dicts |
| `workflow` | List of simulation/calculation steps |
| `operation` | List of atomic-scale transforms |
| `activity` | Legacy alias for `operation` (parser still accepts it) |
| `math_operation` | List of arithmetic activities |
| `dataset` | DCAT dataset block (single dict) |

## `workflow.method`

| Value | Meaning |
| ----- | ------- |
| `MolecularDynamics` | Molecular dynamics simulation |
| `MolecularStatics`  | Energy minimisation / static relaxation |
| `DensityFunctionalTheory` | DFT calculation |

## `workflow.algorithm`

| Value | Notes |
| ----- | ----- |
| `EquationOfStateFit` | |
| `QuasiHarmonicApproximation` | |
| `ThermodynamicIntegration` | |
| `ANNNIModel` | |
| `TensileTest` | Canonical |
| `CompressionTest` | |
| `UniaxialTension` | Legacy alias → `TensileTest` (still accepted) |

## `workflow.degrees_of_freedom`

| Value | |
| ----- | --- |
| `AtomicPositionRelaxation` | |
| `CellVolumeRelaxation` | |
| `CellShapeRelaxation` | |

## `workflow.thermodynamic_ensemble`

| Value | Common short name |
| ----- | ----------------- |
| `CanonicalEnsemble` | NVT |
| `MicrocanonicalEnsemble` | NVE |
| `IsothermalIsobaricEnsemble` | NPT |
| `IsoenthalpicIsobaricEnsemble` | NPH |
| `GrandCanonicalEnsemble` | μVT |

## `workflow.xc_functional`

| Canonical | Aliases |
| --------- | ------- |
| `LocalDensityApproximation` | `LDA` |
| `GeneralizedGradientApproximation` | `GGA`, `PBE`, `PerdewBurkeErnzerhof` |
| `MetaGeneralizedGradientApproximation` | |
| `HybridFunctional` | |
| `HybridGeneralizedGradientApproximation` | |
| `HybridMetaGeneralizedGradientApproximation` | |

Unknown strings fall back to a generic `XCFunctional` node in atomRDF without
error, but `validate(strict=True)` still flags them so typos surface during
authoring.

## `interatomic_potential.potential_type`

| Canonical | Aliases (LAMMPS / common) |
| --------- | ------------------------- |
| `InteratomicPotential` | — (generic) |
| `EmbeddedAtomModel` | `EAM`, `eam`, `eam/alloy`, `eam/fs` |
| `ModifiedEmbeddedAtomModel` | `MEAM`, `meam` |
| `LennardJonesPotential` | `LJ`, `lj` |
| `MachineLearningPotential` | `ACE`, `pace`, `HDNNP`, `hdnnp`, `grace`, `GRACE` |

## `operation.method`

| Value | Required fields | Aliases |
| ----- | --------------- | ------- |
| `DeleteAtom` | `input_sample`, `output_sample` | |
| `SubstituteAtom` | `input_sample`, `output_sample` | |
| `AddAtom` | `input_sample`, `output_sample` | |
| `Rotate` | `rotation_matrix` | `Rotation` |
| `Translate` | `translation_vector` | `Translation` |
| `Shear` | `shear_vector` (and optionally `normal_vector`, `distance`) | |

The `operation` section may also be written under the legacy key `activity`.

## `math_operation.type`

| Value | Required operand fields |
| ----- | ----------------------- |
| `Subtraction` | `minuend`, `subtrahend` |
| `Addition` | `addend` (list, length ≥ 2) |
| `Multiplication` | `factor` (list, length ≥ 2) |
| `Division` | `dividend`, `divisor` |
| `Exponentiation` | `base`, `exponent` |

Operands accept either a numeric scalar **or** the `id` string of a property
declared earlier in `calculated_property` / `input_parameter` /
`output_parameter`. The `result` block is itself a property and may carry an
`id` that downstream math operations reference.

## Property `label` / `basename`

`label` is the canonical key; `basename` is kept as a backwards-compatible
alias. atomRDF resolves the value against ASMO classes — these are the strings
known to round-trip cleanly:

| Label | Typical unit | Notes |
| ----- | ------------ | ----- |
| `TotalEnergy` | `EV` | |
| `EquilibriumEnergy` | `EV` | Energy at minimum |
| `KineticEnergy` | `EV` | |
| `PotentialEnergy` | `EV` | |
| `Temperature` | `K` | |
| `Pressure` | `PA` | |
| `Stress` | `PA` | |
| `Strain` | `M_PER_M` | dimensionless ratio |
| `Volume` | `ANGSTROM3` | |
| `LatticeParameter` | `ANGSTROM` | |
| `BulkModulus` | `PA` | |
| `C11`, `C12`, `C44` | `PA` | Elastic constants |
| `FormationEnergy` | `EV` | Often produced via `math_operation` |
| `VacancyFormationEnergy` | `EV` | |
| `MigrationEnergy` | `EV` | |
| `SegregationEnergy` | `EV` | |
| `StackingFaultEnergy` | `J_PER_M2` | |
| `SurfaceEnergy` | `J_PER_M2` | |
| `GrainBoundaryEnergy` | `J_PER_M2` | |
| `WorkOfSeparation` | `J_PER_M2` | |

Unknown labels are still serialised — they just won't auto-link to an ASMO
class in the resulting RDF graph.

## Property `unit` (QUDT codes)

`unit` strings are QUDT codes (uppercase, e.g. `EV`, `K`, `PA`,
`ANGSTROM3`, `J_PER_M2`, `M_PER_M`). atomRDF resolves them at parse time;
unknown values are stored verbatim. There is no closed enumeration here —
prefer the QUDT canonical code when one exists.

## Defect keys

| YAML key | Category |
| -------- | -------- |
| `vacancy`, `substitutional`, `interstitial` | Point defect (PODO) |
| `stacking_fault` | Planar (PLDO) |
| `grain_boundary`, `tilt_grain_boundary`, `twist_grain_boundary`, `symmetric_tilt_grain_boundary`, `mixed_grain_boundary` | Planar (PLDO) |
| `dislocation`, `edge_dislocation`, `screw_dislocation`, `mixed_dislocation` | Line (LDO) |
| `defect_complex` | Composite (CDCO) |

`mixed_dislocation` adds a `character_angle` field (degrees).

## `atom_attribute` file fields

For systems too big to inline, pass a structure file instead:

| Field | Notes |
| ----- | ----- |
| `file_path` | Path or URI to the structure file |
| `file_format` | ASE format string (e.g. `lammps-data`, `vasp`, `cif`) |
| `file_species` | Ordered list of element symbols matching numeric LAMMPS atom types |

## `software` / `workflow_manager`

Each entry is a dict:

```python
{"uri": "https://www.lammps.org/", "version": "29Aug2024", "label": "LAMMPS"}
```

`software` is a list (multiple binaries per workflow step are fine);
`workflow_manager` is a single dict.
