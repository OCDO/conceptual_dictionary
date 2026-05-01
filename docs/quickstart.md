# Quick start

The minimum useful document is one sample plus one workflow that produced a
calculated property. We build it from the templates, validate it, and write
it to YAML and JSON.

```python
import copy
from conceptual_dictionary import (
    ConceptualDict,
    sample_template,
    workflow_template,
    property_template,
    dataset_template,
)

cd = ConceptualDict()

# ── 1. A sample ───────────────────────────────────────────────────────────────
sample = copy.deepcopy(sample_template)
sample["id"] = "Al_fcc"
sample["material"]["element_ratio"] = {"Al": 1.0}
sample["material"]["crystal_structure"]["spacegroup_symbol"] = "Fm-3m"
sample["material"]["crystal_structure"]["spacegroup_number"] = 225
sample["material"]["crystal_structure"]["unit_cell"]["lattice_parameter"] = [4.05, 4.05, 4.05]
sample["material"]["crystal_structure"]["unit_cell"]["angle"] = [90.0, 90.0, 90.0]
cd["computational_sample"].append(sample)

# ── 2. A workflow step that produced an EquilibriumEnergy property ──────────
wf = copy.deepcopy(workflow_template)
wf["method"] = "MolecularStatics"
wf["interatomic_potential"] = {
    "potential_type": "eam/alloy",
    "uri": "https://doi.org/10.1103/physrevb.59.3393",
}
wf["input_sample"]  = ["Al_fcc"]
wf["output_sample"] = ["Al_fcc"]

energy = copy.deepcopy(property_template)
energy.update({
    "label": "EquilibriumEnergy",
    "value": -3.36,
    "unit": "EV",
    "associate_to_sample": ["Al_fcc"],
})
wf["calculated_property"] = [energy]
cd["workflow"].append(wf)

# ── 3. Optional dataset provenance (DCAT) ────────────────────────────────────
ds = copy.deepcopy(dataset_template)
ds["title"]   = "Al FCC reference"
ds["samples"] = ["Al_fcc"]
cd["dataset"] = ds

# ── 4. Validate against atomRDF's controlled vocabularies ───────────────────
cd.validate(strict=True)            # raises on the first violation, if any

# ── 5. Persist ──────────────────────────────────────────────────────────────
cd.to_yaml("metadata.yaml")
cd.to_json("metadata.json", indent=2)
```

The resulting `metadata.yaml` is consumable by atomRDF directly:

```python
from atomrdf.io.workflow_parser import WorkflowParser
from atomrdf import KnowledgeGraph

kg = KnowledgeGraph()
WorkflowParser(graph=kg).parse_file("metadata.yaml")
```

## Loading back

```python
from conceptual_dictionary import ConceptualDict

cd2 = ConceptualDict.from_yaml("metadata.yaml")
cd3 = ConceptualDict.from_json("metadata.json")
```

Both class-methods accept partial files — any top-level section that is missing
keeps its default empty list.

## Next steps

- See [](templates.md) for every field of every template.
- See [](vocabularies.md) for the full list of accepted strings (methods,
  algorithms, ensembles, potentials, XC functionals, operations, math
  operations, defect keys).
- See [](examples.md) for a notebook that builds the bundled `examples/*.yaml`
  files end-to-end.
