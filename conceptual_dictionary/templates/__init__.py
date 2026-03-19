"""
conceptual_dictionary.templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Re-exports every template from the categorised sub-modules so that
``from conceptual_dictionary.templates import sample_template`` (and every
other name) continues to work exactly as before.
"""

from conceptual_dictionary.templates.sample import sample_template
from conceptual_dictionary.templates.property import property_template
from conceptual_dictionary.templates.workflow import workflow_template
from conceptual_dictionary.templates.dataset import dataset_template
from conceptual_dictionary.templates.operations import (
    math_operation_template,
    operation_template,
)
from conceptual_dictionary.templates.defects import (
    vacancy_template,
    substitutional_template,
    interstitial_template,
    grain_boundary_template,
    dislocation_template,
    stacking_fault_template,
    defect_complex_template,
)
from conceptual_dictionary.templates.full import (
    full_sample_template,
    full_yaml_template,
)

__all__ = [
    "sample_template",
    "property_template",
    "workflow_template",
    "dataset_template",
    "math_operation_template",
    "operation_template",
    "vacancy_template",
    "substitutional_template",
    "interstitial_template",
    "grain_boundary_template",
    "dislocation_template",
    "stacking_fault_template",
    "defect_complex_template",
    "full_sample_template",
    "full_yaml_template",
]
