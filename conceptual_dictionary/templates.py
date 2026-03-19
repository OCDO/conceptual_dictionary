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

# ── Point-defect templates ────────────────────────────────────────────────────
# Use exactly ONE of `vacancy`, `substitutional`, or `interstitial` as a key
# directly inside the sample dict (alongside material / simulation_cell etc.).
# `point_defect` is a generic base and rarely needed on its own.

vacancy_template = {
    "concentration": None,  # atomic fraction (float), e.g. 0.004
    "number": None,  # integer count of vacancies, e.g. 1
}

substitutional_template = {
    "concentration": None,  # impurity concentration (atomic fraction), e.g. 0.01
    "number": None,  # integer count of substitutional atoms, e.g. 2
}

interstitial_template = {
    "concentration": None,  # impurity concentration (atomic fraction), e.g. 0.005
    "number": None,  # integer count of interstitial atoms, e.g. 1
}

# ── Stacking-fault template ───────────────────────────────────────────────────
# Use key `stacking_fault` directly inside the sample dict.

stacking_fault_template = {
    "plane": None,  # Miller indices of the fault plane, e.g. [1, 1, 1]
    "displacement": None,  # displacement (shift) vector, e.g. [0.5, 0.5, 0.0]
}

# ── Grain-boundary templates ──────────────────────────────────────────────────
# All five GB subtypes share the same fields below.  Choose the key that
# matches the physical character of the boundary:
#   grain_boundary                  — generic (unspecified type)
#   tilt_grain_boundary             — pure tilt
#   twist_grain_boundary            — pure twist
#   symmetric_tilt_grain_boundary   — symmetric tilt
#   mixed_grain_boundary            — mixed tilt+twist
#
# Place the chosen key directly inside the sample dict.

grain_boundary_template = {
    "sigma": None,  # CSL sigma value (integer), e.g. 3
    "plane": None,  # GB plane Miller indices, e.g. [1.0, 1.0, 2.0]
    "misorientation_angle": None,  # misorientation angle in degrees, e.g. 38.94
    "rotation_axis": None,  # rotation axis (Miller indices), e.g. [1, 1, 0]
}

# ── Dislocation templates ─────────────────────────────────────────────────────
# `dislocation`, `edge_dislocation`, and `screw_dislocation` all use the fields
# below.  `mixed_dislocation` additionally accepts `character_angle`.
# Place the chosen key directly inside the sample dict.

dislocation_template = {
    "line_direction": None,  # dislocation line direction vector, e.g. [1, 0, 0]
    "burgers_vector": None,  # Burgers vector, e.g. [0.5, 0.5, 0.0]
    "slip_system": {
        "slip_direction": None,  # slip direction vector, e.g. [1, 1, 0]
        "slip_plane": {
            "normal": None,  # slip-plane normal vector, e.g. [1, 1, 1]
        },
    },
    # Only required for mixed_dislocation:
    # "character_angle": None,  # character angle in degrees (float), e.g. 45.0
}

# ── Defect-complex template ───────────────────────────────────────────────────
# Marks two or more co-existing defects as forming a complex.
# `ids` lists the YAML key names of the constituent defects used in the
# same sample (e.g. ["vacancy", "substitutional"]).
# Place key `defect_complex` directly inside the sample dict alongside the
# individual defect keys.

defect_complex_template = {
    "ids": [],  # defect YAML key names forming the complex,
    # e.g. ["vacancy", "substitutional"]
    "relative_distance": None,  # distance between defects (string with unit),
    # e.g. "2.5 Å"
}

# ═════════════════════════════════════════════════════════════════════════════
# FULL TEMPLATES — complete reference showing every key in its proper place
# ═════════════════════════════════════════════════════════════════════════════

# full_sample_template — every possible field that belongs inside a sample.
# All defect keys are optional; use at most one per category.
# Grain-boundary alternatives: grain_boundary | tilt_grain_boundary |
#   twist_grain_boundary | symmetric_tilt_grain_boundary | mixed_grain_boundary
# Dislocation alternatives: dislocation | edge_dislocation |
#   screw_dislocation | mixed_dislocation  (mixed adds "character_angle")
full_sample_template = {
    # ── Identity ──────────────────────────────────────────────────────────────
    "id": "sample1",
    # ── Material description ──────────────────────────────────────────────────
    "material": {
        "element_ratio": {},  # e.g. {"Al": 1.0} or {"Fe": 0.8, "Cr": 0.2}
        "crystal_structure": {
            "spacegroup_symbol": None,  # e.g. "Fm-3m"
            "spacegroup_number": None,  # e.g. 225
            "unit_cell": {
                "bravais_lattice": None,  # ontology URI string
                "lattice_parameter": None,  # [a, b, c] in Å, e.g. [4.05, 4.05, 4.05]
                "angle": [],  # [α, β, γ] in degrees
            },
        },
    },
    # ── Simulation cell ───────────────────────────────────────────────────────
    "simulation_cell": {
        "volume": {"value": None},  # volume in Å³
        "number_of_atoms": None,
        "length": [],  # [lx, ly, lz] in Å
        "vector": [],  # 3×3 cell vectors
        "angle": [],  # [α, β, γ] in degrees
        "repetitions": [],  # supercell repetitions, e.g. [3, 3, 3]
        "grain_size": None,  # average grain size (polycrystal)
        "number_of_grains": 0,  # number of grains (polycrystal)
    },
    # ── Atomic positions / species ────────────────────────────────────────────
    "atom_attribute": {
        # Option A — inline arrays (small systems / test cases)
        "position": None,  # list of [x, y, z] coordinate arrays
        "species": None,  # list of element symbols, e.g. ["Al", "Al", ...]
        # Option B — file reference (preferred for large MD snapshots)
        "file_path": None,  # path relative to YAML, e.g. "../data/snapshot.gz"
        "file_format": None,  # ASE format string, e.g. "lammps-dump-text"
        "file_species": None,  # species order for LAMMPS numeric types, e.g. ["Al"]
    },
    # ── Calculated properties attached directly to the sample ─────────────────
    "calculated_property": [
        # {"id": None, "label": None, "value": None, "unit": None,
        #  "associate_to_sample": []}
    ],
    # ── Defects (all optional — include only what applies) ────────────────────
    # Point defects
    "vacancy": {
        "concentration": None,  # atomic fraction, e.g. 0.004
        "number": None,  # integer count, e.g. 1
    },
    # "substitutional": {"concentration": None, "number": None},
    # "interstitial":   {"concentration": None, "number": None},
    # Stacking fault:
    # "stacking_fault": {
    #     "plane": None,           # fault plane Miller indices, e.g. [1, 1, 1]
    #     "displacement": None,    # shift vector, e.g. [0.5, 0.5, 0.0]
    # },
    # Grain boundary — use at most ONE of the five variants below:
    # "grain_boundary": {
    #     "sigma": None,                # CSL Σ value (int), e.g. 3
    #     "plane": None,                # GB plane Miller indices, e.g. [1.0, 1.0, 2.0]
    #     "misorientation_angle": None, # degrees, e.g. 38.94
    #     "rotation_axis": None,        # Miller indices, e.g. [1, 1, 0]
    # },
    # other variants: tilt_grain_boundary | twist_grain_boundary |
    #                 symmetric_tilt_grain_boundary | mixed_grain_boundary
    # (all use the same four fields above)
    # Dislocation — use at most ONE of the four variants below:
    # "dislocation": {                  # also: edge_dislocation, screw_dislocation
    #     "line_direction": None,       # line direction vector, e.g. [1, 0, 0]
    #     "burgers_vector": None,       # Burgers vector, e.g. [0.5, 0.5, 0.0]
    #     "slip_system": {
    #         "slip_direction": None,   # e.g. [1, 1, 0]
    #         "slip_plane": {
    #             "normal": None,       # slip-plane normal, e.g. [1, 1, 1]
    #         },
    #     },
    #     # "character_angle": None,    # mixed_dislocation only (degrees)
    # },
    # Defect complex — combine with any defect keys above:
    # "defect_complex": {
    #     "ids": [],                    # e.g. ["vacancy", "substitutional"]
    #     "relative_distance": None,    # e.g. "2.5 Å"
    # },
}

# full_yaml_template — mirrors the complete top-level structure of a YAML file.
# Every section is optional except that at least one of samples / workflow must
# be present for the file to be meaningful.
full_yaml_template = {
    # ── Dataset provenance (optional but recommended) ─────────────────────────
    "dataset": {
        "identifier": None,  # dataset URI, e.g. "https://doi.org/10.5281/zenodo.1234567"
        "title": None,  # e.g. "Grain boundary energies for Al"
        "creators": [
            {
                "id": None,  # ORCID URI, e.g. "https://orcid.org/0000-0000-0000-0000"
                "name": None,  # e.g. "Abril Guzman"
            }
        ],
        "publication": {
            "id": None,  # publication URI
            "identifier": None,  # DOI string, e.g. "10.1016/j.actamat.2024.12345"
            "title": None,
        },
        "samples": [],  # list of sample IDs belonging to this dataset
    },
    # ── Samples — one entry per simulation snapshot / structure ───────────────
    "samples": [full_sample_template],
    # ── Workflow steps — one entry per simulation / calculation ───────────────
    "workflow": [
        {
            "algorithm": None,  # e.g. "MolecularDynamics"
            "method": None,  # e.g. "LennardJonesPotential"
            "xc_functional": None,  # DFT only, e.g. "PBE"
            "input_parameter": [
                # {"id": None, "label": None, "value": None, "unit": None}
            ],
            "input_sample": [],  # list of sample IDs consumed by this step
            "output_sample": [],  # list of sample IDs produced by this step
            "output_parameter": [
                # {"id": None, "label": None, "value": None, "unit": None}
            ],
            "calculated_property": [
                # {"id": None, "label": None, "value": None, "unit": None,
                #  "associate_to_sample": []}
            ],
            "degrees_of_freedom": [],  # e.g. ["AtomicScalePosition"]
            "interatomic_potential": {
                "potential_type": None,  # e.g. "EAM"
                "uri": None,  # OpenKIM URI or similar
            },
            "software": [
                # {"uri": None, "version": None, "label": None}
            ],
            "workflow_manager": {
                "uri": None,
                "version": None,
                "label": None,
            },
            "thermodynamic_ensemble": None,  # e.g. "NVT"
        }
    ],
    # ── Atomic-scale transform operations (optional) ──────────────────────────
    "operation": [
        {
            "method": None,  # DeleteAtom | SubstituteAtom | AddAtom |
            # Rotate | Translate | Shear
            "input_sample": None,
            "output_sample": None,
            # method-specific fields (include only what applies):
            "rotation_matrix": None,  # Rotate: 3×3 matrix
            "translation_vector": None,  # Translate: [x, y, z]
            "shear_vector": None,  # Shear: [x, y, z]
            "normal_vector": None,  # Shear (optional): [x, y, z]
            "distance": None,  # Shear (optional): float
        }
    ],
    # ── Math operations — derived quantities from stored properties ───────────
    "math_operation": [
        {
            "type": None,  # Subtraction | Addition | Multiplication |
            # Division | Exponentiation
            "result": {
                "id": None,
                "label": None,
                "value": None,
                "unit": None,
                "associate_to_sample": [],
            },
            # Subtraction:  "minuend": None, "subtrahend": None
            # Addition:     "addend": []
            # Multiplication: "factor": []
            # Division:     "dividend": None, "divisor": None
            # Exponentiation: "base": None, "exponent": None
        }
    ],
}
