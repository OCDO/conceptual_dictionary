"""Validation against controlled vocabularies."""
import copy
import warnings

import pytest

from conceptual_dictionary import (
    ConceptualDict,
    workflow_template,
    operation_template,
    math_operation_template,
)


def _wf(**overrides):
    wf = copy.deepcopy(workflow_template)
    wf.update(overrides)
    return wf


def test_empty_validates_clean():
    cd = ConceptualDict()
    assert cd.validate() == []


def test_valid_workflow_passes():
    cd = ConceptualDict()
    cd["workflow"].append(_wf(
        method="MolecularStatics",
        algorithm="EquationOfStateFit",
        thermodynamic_ensemble="CanonicalEnsemble",
        xc_functional="PBE",
        degrees_of_freedom=["AtomicPositionRelaxation", "CellVolumeRelaxation"],
        interatomic_potential={"potential_type": "eam/alloy", "uri": "x"},
    ))
    assert cd.validate() == []


def test_invalid_method_warns_and_reports():
    cd = ConceptualDict()
    cd["workflow"].append(_wf(method="NotAMethod"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        violations = cd.validate()
    assert any("NotAMethod" in str(w.message) for w in caught)
    assert len(violations) == 1
    v = violations[0]
    assert v["section"] == "workflow"
    assert v["index"] == 0
    assert v["field"] == "method"
    assert v["value"] == "NotAMethod"
    assert isinstance(v["allowed"], frozenset)


def test_invalid_method_strict_raises():
    cd = ConceptualDict()
    cd["workflow"].append(_wf(method="Bogus"))
    with pytest.raises(ValueError, match="Bogus"):
        cd.validate(strict=True)


def test_list_field_validates_each_entry():
    cd = ConceptualDict()
    cd["workflow"].append(_wf(degrees_of_freedom=["AtomicPositionRelaxation",
                                                  "BogusDoF"]))
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        violations = cd.validate()
    assert len(violations) == 1
    assert violations[0]["value"] == "BogusDoF"


def test_potential_type_alias_accepted():
    """LAMMPS pair_style strings used as potential_type aliases."""
    cd = ConceptualDict()
    for alias in ("EAM", "eam", "eam/alloy", "eam/fs", "MEAM", "LJ"):
        cd["workflow"].append(_wf(
            interatomic_potential={"potential_type": alias, "uri": "x"},
        ))
    assert cd.validate() == []


def test_xc_functional_canonical_and_alias():
    cd = ConceptualDict()
    for xc in ("LDA", "GGA", "PBE", "HybridFunctional",
               "MetaGeneralizedGradientApproximation"):
        cd["workflow"].append(_wf(xc_functional=xc))
    assert cd.validate() == []


def test_operation_method_validation():
    cd = ConceptualDict()
    op = copy.deepcopy(operation_template)
    op["method"] = "Rotation"   # alias for Rotate
    cd["operation"].append(op)
    assert cd.validate() == []

    bad = copy.deepcopy(operation_template)
    bad["method"] = "NopeOp"
    cd["operation"].append(bad)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        violations = cd.validate()
    assert len(violations) == 1
    assert violations[0]["section"] == "operation"


def test_math_operation_type_validation():
    cd = ConceptualDict()
    mo = copy.deepcopy(math_operation_template)
    mo["type"] = "NotAnOp"
    cd["math_operation"].append(mo)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        violations = cd.validate()
    assert len(violations) == 1
    assert violations[0]["field"] == "type"


def test_uniaxial_tension_alias_accepted():
    cd = ConceptualDict()
    cd["workflow"].append(_wf(algorithm="UniaxialTension"))
    assert cd.validate() == []
