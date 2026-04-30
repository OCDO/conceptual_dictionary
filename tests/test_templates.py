"""Templates: structural sanity and parity with atomRDF parser keys."""
import copy

from conceptual_dictionary import (
    sample_template,
    workflow_template,
    property_template,
    dataset_template,
    operation_template,
    math_operation_template,
    grain_boundary_template,
    dislocation_template,
    stacking_fault_template,
    vacancy_template,
    full_yaml_template,
    full_sample_template,
)


def test_sample_template_top_level_keys():
    expected = {"id", "material", "simulation_cell",
                "atom_attribute", "calculated_property"}
    assert expected.issubset(sample_template.keys())


def test_sample_template_atom_attribute_supports_file_reference():
    aa = sample_template["atom_attribute"]
    for key in ("position", "species", "file_path", "file_format", "file_species"):
        assert key in aa, f"atom_attribute missing key: {key}"


def test_workflow_template_keys_match_atomrdf_parser():
    expected = {
        "method", "algorithm", "xc_functional", "input_parameter",
        "input_sample", "output_sample", "output_parameter",
        "calculated_property", "degrees_of_freedom", "interatomic_potential",
        "software", "workflow_manager", "thermodynamic_ensemble",
    }
    assert expected.issubset(workflow_template.keys())


def test_workflow_potential_shape():
    pot = workflow_template["interatomic_potential"]
    assert "potential_type" in pot
    assert "uri" in pot


def test_workflow_manager_is_dict_with_uri_version_label():
    wm = workflow_template["workflow_manager"]
    assert isinstance(wm, dict)
    assert {"uri", "version", "label"}.issubset(wm.keys())


def test_property_template_has_id_for_cross_reference():
    """Property id is what later math_operation entries reference as an operand."""
    assert "id" in property_template
    for k in ("label", "value", "unit", "associate_to_sample"):
        assert k in property_template


def test_dataset_template_dcat_shape():
    expected = {"identifier", "title", "creators", "publication", "samples"}
    assert expected.issubset(dataset_template.keys())
    assert isinstance(dataset_template["creators"], list)
    pub = dataset_template["publication"]
    assert {"id", "identifier", "title"}.issubset(pub.keys())


def test_operation_template_has_all_method_specific_fields():
    expected = {"method", "input_sample", "output_sample",
                "rotation_matrix", "translation_vector",
                "shear_vector", "normal_vector", "distance"}
    assert expected.issubset(operation_template.keys())


def test_math_operation_template_has_all_operand_fields():
    expected = {"type", "result",
                "minuend", "subtrahend",        # Subtraction
                "addend",                       # Addition
                "factor",                       # Multiplication
                "dividend", "divisor",          # Division
                "base", "exponent"}             # Exponentiation
    assert expected.issubset(math_operation_template.keys())


def test_defect_template_field_sets():
    assert {"sigma", "plane", "misorientation_angle", "rotation_axis"} \
        == set(grain_boundary_template.keys())
    assert {"line_direction", "burgers_vector", "slip_system"} \
        .issubset(dislocation_template.keys())
    assert {"plane", "displacement"} == set(stacking_fault_template.keys())
    assert {"concentration", "number"} == set(vacancy_template.keys())


def test_full_yaml_template_uses_computational_sample_key():
    """Regression test for the 0.3.1 fix: must NOT use 'samples' at top level."""
    assert "computational_sample" in full_yaml_template
    assert "samples" not in full_yaml_template


def test_full_sample_template_includes_defect_blocks():
    # at minimum the example vacancy block should be present
    assert "vacancy" in full_sample_template


def test_templates_are_independent_copies():
    """Mutating a deepcopy must not bleed back into the canonical template."""
    s = copy.deepcopy(sample_template)
    s["id"] = "mutated"
    s["material"]["element_ratio"]["Mutant"] = 99
    assert sample_template["id"] != "mutated"
    assert "Mutant" not in sample_template["material"]["element_ratio"]
