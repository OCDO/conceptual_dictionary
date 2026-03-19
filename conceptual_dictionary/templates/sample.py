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
        "file_path": None,  # path to structure file, e.g. '../data/snapshot.gz'
        "file_format": None,  # ASE format string, e.g. 'lammps-dump-text' (auto-detected if None)
        "file_species": None,  # species order for LAMMPS numeric types, e.g. ['Al']
    },
    "calculated_property": [],
}
