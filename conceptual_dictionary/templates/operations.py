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

# Operation template for atomic-scale transformations.
# Contains all possible fields for all operation types; include only what applies.
operation_template = {
    "method": None,  # Required: DeleteAtom | SubstituteAtom | AddAtom |
    #           Rotate | Translate | Shear
    "input_sample": None,  # Required
    "output_sample": None,  # Required
    # Optional fields (used by specific operations):
    "rotation_matrix": None,  # Rotate: 3×3 matrix, e.g. [[1,0,0],[0,1,0],[0,0,1]]
    "translation_vector": None,  # Translate: 3D vector, e.g. [1.5, 2.0, 0.5]
    "shear_vector": None,  # Shear: 3D vector, e.g. [0.1, 0, 0]
    "normal_vector": None,  # Shear (optional): 3D vector, e.g. [1, 1, 1]
    "distance": None,  # Shear (optional): float
}
