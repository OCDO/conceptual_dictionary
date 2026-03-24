# conceptual_dictionary

A Python dictionary template for storing structured, serializable metadata in a lightweight, ontology-aligned format for simulation data and workflows.

## Installation

Install from source:

```bash
pip install -e .
```

## Usage

### Using Templates

Import and use predefined dictionary templates:

```python
from conceptual_dictionary.templates import sample_template, property_template, workflow_template

# Use a template directly
my_data = sample_template.copy()
my_data['material']['element_ratio'] = {'Fe': 0.7, 'C': 0.3}
my_data['simulation_cell']['volume']['value'] = 1000
```

### Using ConceptualDict Class

Work with conceptual dictionaries using the ConceptualDict class:

```python
from conceptual_dictionary.conceptualdict import ConceptualDict

# Create a new conceptual dictionary
cd = ConceptualDict()

# Set values using dot notation
cd.set("material.element_ratio.Fe", 0.7)
cd.set("material.element_ratio.C", 0.3)
cd.set("simulation_cell.volume.value", 1000)

# Get values
fe_ratio = cd.get("material.element_ratio.Fe")
volume = cd.get("simulation_cell.volume.value")

# Convert to standard dictionary
data = cd.to_dict()

# Serialize to JSON
json_str = cd.to_json(indent=2)

# Save to file
cd.save("my_conceptual.json")

# Load from file
cd_loaded = ConceptualDict.from_json("my_conceptual.json")
```

## Available Templates

- **sample_template**: Standard template with metadata, content, and schema sections
- **property_template**: Template for defining properties with values and units
- **workflow_template**: Template for describing workflows, including algorithms and methods
- **operation_template**: Unified template for all atomic-scale operations (DeleteAtom, SubstituteAtom, AddAtom, Rotate, Translate, Shear) with all possible fields

### Using Operation Template

```python
from conceptual_dictionary.templates import operation_template

# Create a rotation operation
rotation_op = operation_template.copy()
rotation_op['method'] = 'Rotate'
rotation_op['input_sample'] = 'sample1'
rotation_op['output_sample'] = 'sample2'
rotation_op['rotation_matrix'] = [[1.0, 0.0, 0.0], [0.0, 0.707, -0.707], [0.0, 0.707, 0.707]]

# Create a translation operation
translation_op = operation_template.copy()
translation_op['method'] = 'Translate'
translation_op['input_sample'] = 'sample2'
translation_op['output_sample'] = 'sample3'
translation_op['translation_vector'] = [1.5, 2.0, 0.5]

# Create a simple delete operation
delete_op = operation_template.copy()
delete_op['method'] = 'DeleteAtom'
delete_op['input_sample'] = 'sample3'
delete_op['output_sample'] = 'sample4'

# Add to ConceptualDict
cd = ConceptualDict()
cd['operation'].append(rotation_op)
cd['operation'].append(translation_op)
cd['operation'].append(delete_op)
```

## License

MIT License
