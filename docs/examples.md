# Examples

The bundled notebook walks through building a single-crystal sample with a
full workflow + property record, and then a more elaborate grain-boundary
case with explicit defect blocks.

::::{grid} 1 1 2 2
:class-container: text-center
:gutter: 3

:::{grid-item-card}
:link: ../examples/examples
:link-type: doc
:class-header: bg-light
End-to-end notebook
^^^
Build, validate, write and round-trip the bundled
`single_structure_with_workflow.yaml` and `grain_boundary.yaml` files.
:::

::::

The matching reference YAML/JSON files live next to the notebook:

| File | What it shows |
| ---- | ------------- |
| `examples/single_structure_with_workflow.yaml` | One sample + one MD workflow + a calculated property |
| `examples/grain_boundary.yaml` | A grain-boundary sample with `tilt_grain_boundary` defect block |
| `examples/single_structure_with_workflow.json` | Same content, JSON variant |
| `examples/grain_boundary.json` | Same content, JSON variant |
