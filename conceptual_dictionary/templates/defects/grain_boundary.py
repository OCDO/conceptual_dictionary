# All five GB subtypes share the same fields.  Choose the YAML key that
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
