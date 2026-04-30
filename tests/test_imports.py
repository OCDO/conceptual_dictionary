"""Smoke tests: every public name in __all__ imports cleanly."""
import conceptual_dictionary as cd


def test_package_exports():
    for name in cd.__all__:
        assert hasattr(cd, name), f"missing public export: {name}"


def test_templates_are_dicts():
    template_names = [
        "sample_template", "property_template", "workflow_template",
        "dataset_template", "operation_template", "math_operation_template",
        "vacancy_template", "substitutional_template", "interstitial_template",
        "stacking_fault_template", "grain_boundary_template",
        "dislocation_template", "defect_complex_template",
        "full_sample_template", "full_yaml_template",
    ]
    for name in template_names:
        assert isinstance(getattr(cd, name), dict), f"{name} should be a dict"


def test_vocabularies_are_frozensets():
    vocab_names = [
        "METHOD", "ALGORITHM", "DEGREES_OF_FREEDOM", "THERMODYNAMIC_ENSEMBLE",
        "POTENTIAL_TYPE", "XC_FUNCTIONAL", "OPERATION_METHOD",
        "MATH_OPERATION_TYPE", "GRAIN_BOUNDARY_TYPE", "YAML_TOP_LEVEL_KEYS",
    ]
    for name in vocab_names:
        v = getattr(cd, name)
        assert isinstance(v, frozenset), f"{name} should be a frozenset"
        assert len(v) > 0, f"{name} is empty"


def test_controlled_values_map():
    assert isinstance(cd.CONTROLLED_VALUES, dict)
    for key, (allowed, scope) in cd.CONTROLLED_VALUES.items():
        assert isinstance(allowed, frozenset)
        assert isinstance(scope, str)
