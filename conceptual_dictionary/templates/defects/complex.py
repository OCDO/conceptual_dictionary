# Marks two or more co-existing defects as forming a complex.
# `ids` lists the YAML key names of the constituent defects present in the
# same sample (e.g. ["vacancy", "substitutional"]).
# Place key `defect_complex` directly inside the sample dict alongside the
# individual defect keys.

defect_complex_template = {
    "ids": [],  # defect YAML key names forming the complex,
    # e.g. ["vacancy", "substitutional"]
    "relative_distance": None,  # distance between defects (string with unit),
    # e.g. "2.5 Å"
}
