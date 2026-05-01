# conceptual_dictionary

`conceptual_dictionary` is a Python package providing **strongly-typed dictionary
templates and controlled vocabularies** for serialising
computational-materials-science metadata to YAML or JSON.

The schema and vocabularies are kept in lock-step with
[atomRDF](https://github.com/pyscal/atomRDF), so files produced with
`conceptual_dictionary` are parsed directly by atomRDF's `WorkflowParser` —
no glue code, no field renaming.

The dictionaries cover the same OCDO ontologies that atomRDF builds RDF
graphs from:

| Ontology | What it covers |
| -------- | -------------- |
| **CMSO** | Computational Material Sample Ontology |
| **CDCO** | Crystallographic Defect Core Ontology |
| **PODO** | Point-defect Ontology |
| **PLDO** | Planar-defect Ontology |
| **LDO**  | Line-defect Ontology |
| **ASMO** | Atomistic Simulation Methods Ontology |

Every template is a plain `dict` — copy it, fill in what applies, drop into
[`ConceptualDict`](docs/conceptualdict.md), and serialise. Optional runtime
[validation](docs/validation.md) catches typos against the controlled
vocabularies.

## Where to next

- [](docs/gettingstarted.md) — install in pip / conda / from source.
- [](docs/quickstart.md) — build, validate and write your first metadata file.
- [](docs/templates.md) — every template field explained.
- [](docs/conceptualdict.md) — `ConceptualDict` API and round-trip I/O.
- [](docs/vocabularies.md) — every accepted string, cross-referenced with atomRDF.
- [](docs/validation.md) — strict & non-strict checking.
- [](docs/examples.md) — worked notebook covering a full single-crystal +
  workflow case and a grain-boundary case.
- [](docs/api.rst) — full API reference.
- [](docs/extending.md) — contribute / extend.

## Citing conceptual_dictionary

If you use `conceptual_dictionary` in academic work, please cite the associated
paper:

> Guzmán, A. A., Menon, S., Hickel, T., & Sandfeld, S. (2026).
> *Ontology-based knowledge graph infrastructure for interoperable atomistic
> simulation data.* arXiv:2604.06230.
> <https://arxiv.org/abs/2604.06230>

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
