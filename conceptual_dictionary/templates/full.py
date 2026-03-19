"""
full_sample_template and full_yaml_template — single-file reference showing
every key in its correct nested position.  Use these as a complete schema
guide; copy and trim to build an actual YAML file.
"""

from conceptual_dictionary.templates.sample import (
    sample_template,
)  # noqa: F401 (re-used below)

# ── full_sample_template ──────────────────────────────────────────────────────
# Every possible field that can appear inside a sample entry.
# All defect keys are optional; include at most ONE per category.
#
# Grain-boundary variants (same four fields, different YAML key):
#   grain_boundary | tilt_grain_boundary | twist_grain_boundary |
#   symmetric_tilt_grain_boundary | mixed_grain_boundary
#
# Dislocation variants (same fields, different YAML key):
#   dislocation | edge_dislocation | screw_dislocation | mixed_dislocation
#   (mixed_dislocation additionally accepts "character_angle")

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
    # Point defects — use at most ONE of the three keys below:
    "vacancy": {
        "concentration": None,  # atomic fraction, e.g. 0.004
        "number": None,  # integer count, e.g. 1
    },
    # "substitutional": {"concentration": None, "number": None},
    # "interstitial":   {"concentration": None, "number": None},
    # Stacking fault:
    # "stacking_fault": {
    #     "plane": None,        # fault plane Miller indices, e.g. [1, 1, 1]
    #     "displacement": None, # shift vector, e.g. [0.5, 0.5, 0.0]
    # },
    # Grain boundary — use at most ONE of the five variant keys:
    # "grain_boundary": {
    #     "sigma": None,                # CSL Σ value (int), e.g. 3
    #     "plane": None,                # GB plane Miller indices, e.g. [1.0, 1.0, 2.0]
    #     "misorientation_angle": None, # degrees, e.g. 38.94
    #     "rotation_axis": None,        # Miller indices, e.g. [1, 1, 0]
    # },
    # tilt_grain_boundary | twist_grain_boundary |
    # symmetric_tilt_grain_boundary | mixed_grain_boundary — same four fields
    # Dislocation — use at most ONE of the four variant keys:
    # "dislocation": {               # also: edge_dislocation, screw_dislocation
    #     "line_direction": None,    # line direction vector, e.g. [1, 0, 0]
    #     "burgers_vector": None,    # Burgers vector, e.g. [0.5, 0.5, 0.0]
    #     "slip_system": {
    #         "slip_direction": None,  # e.g. [1, 1, 0]
    #         "slip_plane": {
    #             "normal": None,      # slip-plane normal, e.g. [1, 1, 1]
    #         },
    #     },
    #     # "character_angle": None,  # mixed_dislocation only (degrees)
    # },
    # Defect complex — combine with any defect keys above:
    # "defect_complex": {
    #     "ids": [],                 # e.g. ["vacancy", "substitutional"]
    #     "relative_distance": None, # e.g. "2.5 Å"
    # },
}

# ── full_yaml_template ────────────────────────────────────────────────────────
# Mirrors the complete top-level structure of a YAML file.
# Every section is optional; at least one of `samples` / `workflow` should be
# present for the file to be meaningful.

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
            # Subtraction:    "minuend": None, "subtrahend": None
            # Addition:       "addend": []
            # Multiplication: "factor": []
            # Division:       "dividend": None, "divisor": None
            # Exponentiation: "base": None, "exponent": None
        }
    ],
}
