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
    # single-software entry template: {"uri": None, "version": None, "label": None}
    "workflow_manager": {
        "uri": None,
        "version": None,
        "label": None,
    },
    "thermodynamic_ensemble": None,
}
