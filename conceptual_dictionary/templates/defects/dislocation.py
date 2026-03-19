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
    # Only for mixed_dislocation — uncomment when needed:
    # "character_angle": None,  # character angle in degrees (float), e.g. 45.0
}
