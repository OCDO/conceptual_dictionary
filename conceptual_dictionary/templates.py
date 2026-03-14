sample_template = {
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
        # Option A — inline arrays (small systems / test cases)
        "position": None,
        "species": None,
        # Option B — file reference (preferred for large MD snapshots)
        # WorkflowParser resolves this relative to the YAML file's directory.
        "file_path": None,  # path to structure file, e.g. '../DC3_benchmark_data_set/Al_fcc/T_0.10Tm_snapshot_1.gz'
        "file_format": None,  # ASE format string, e.g. 'lammps-dump-text' (auto-detected if None)
        "file_species": None,  # species order for LAMMPS numeric types, e.g. ['Al']
    },
    "calculated_property": [],
}

property_template = {
    "id": None,  # optional local ID; used to reference this property in math_operation operands
    "label": None,  # primary name read by atomRDF WorkflowParser
    "basename": None,  # kept for backwards compat
    "value": None,
    "unit": None,
    "associate_to_sample": [],
}

workflow_template = {
    "algorithm": None,
    "method": None,
    "xc_functional": None,
    # Each entry in these lists may include an optional 'id' field so later
    # math_operation entries can reference the property by its local ID.
    "input_parameter": [
        # {"id": None, "label": None, "basename": None, "value": None, "unit": None}
    ],
    "input_sample": [],
    "output_sample": [],
    "output_parameter": [
        # {"id": None, "label": None, "basename": None, "value": None, "unit": None}
    ],
    "calculated_property": [
        # {"id": None, "label": None, "basename": None, "value": None, "unit": None,
        #  "associate_to_sample": []}
    ],
    "degrees_of_freedom": [],
    "interatomic_potential": {
        "potential_type": None,
        "uri": None,
    },
    # software is a list of {uri, version, label} dicts
    "software": [],
    # single-software template kept for reference:
    # {"uri": None, "version": None, "label": None}
    "workflow_manager": {
        "uri": None,
        "version": None,
        "label": None,
    },
    "thermodynamic_ensemble": None,
}

dataset_template = {
    # dcat:Dataset — the dataset node
    "identifier": None,  # URI/IRI for the dataset, e.g. "https://doi.org/10.5281/zenodo.1234567"
    "title": None,  # dcterms:title, e.g. "Grain boundary energies for Al"
    # dcterms:creator — list of foaf:Person entries
    "creators": [
        {
            "id": None,  # URI for the person, e.g. "https://orcid.org/0000-0000-0000-0000"
            "name": None,  # foaf:name, e.g. "Abril Guzman"
        }
    ],
    # dcterms:isReferencedBy — the associated publication
    "publication": {
        "id": None,  # URI for the paper
        "identifier": None,  # dcterms:identifier — DOI string, e.g. "10.1016/j.actamat.2024.12345"
        "title": None,  # dcterms:title (optional)
    },
    # dcterms:isPartOf — list of sample IDs that belong to this dataset
    # (these are added as triples on each sample: sample dcterms:isPartOf dataset)
    "samples": [],
}

# Math-operation template for ASMO arithmetic activities.
# Operands may be a local property ID string (referencing an earlier
# calculated / input / output property by its 'id' field) or a numeric
# scalar.  The result is a CalculatedProperty and may carry its own 'id'
# so subsequent math_operation entries can use it as an operand.
math_operation_template = {
    "type": None,  # Required: Subtraction | Addition | Multiplication | Division | Exponentiation
    "result": {
        "id": None,  # optional local ID for use as operand in later math operations
        "label": None,
        "basename": None,
        "value": None,  # set if result value is known; otherwise leave None
        "unit": None,
        "associate_to_sample": [],
    },
    # ── Subtraction ──────────────────────────────────────────────────────────
    "minuend": None,  # property ID or scalar
    "subtrahend": None,  # property ID or scalar
    # ── Addition ─────────────────────────────────────────────────────────────
    "addend": [],  # list of property IDs and/or scalars
    # ── Multiplication ───────────────────────────────────────────────────────
    "factor": [],  # list of property IDs and/or scalars
    # ── Division ─────────────────────────────────────────────────────────────
    "dividend": None,  # property ID or scalar
    "divisor": None,  # property ID or scalar
    # ── Exponentiation ───────────────────────────────────────────────────────
    "base": None,  # property ID or scalar
    "exponent": None,  # property ID or scalar
}

# Operation template for atomic-scale transformations
# Contains all possible fields for all operation types
operation_template = {
    "method": None,  # Required: DeleteAtom, SubstituteAtom, AddAtom, Rotate, Translate, Shear
    "input_sample": None,  # Required
    "output_sample": None,  # Required
    # Optional fields (used by specific operations):
    "rotation_matrix": None,  # For Rotate: 3x3 matrix, e.g., [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    "translation_vector": None,  # For Translate: 3D vector, e.g., [1.5, 2.0, 0.5]
    "shear_vector": None,  # For Shear: 3D vector, e.g., [0.1, 0, 0]
    "normal_vector": None,  # For Shear (optional): 3D vector, e.g., [1, 1, 1]
    "distance": None,  # For Shear (optional): float
}
