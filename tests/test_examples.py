"""Bundled example YAML/JSON files load and validate cleanly."""
from pathlib import Path

import pytest

from conceptual_dictionary import ConceptualDict, YAML_TOP_LEVEL_KEYS

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


@pytest.mark.parametrize("name", [
    "single_structure_with_workflow.yaml",
    "grain_boundary.yaml",
])
def test_example_yaml_loads_and_validates(name):
    path = EXAMPLES / name
    if not path.exists():
        pytest.skip(f"example file {name} not present")
    cd = ConceptualDict.from_yaml(str(path))
    # uses only known top-level keys (allow 'dataset' too)
    extra = {"dataset"}
    for key in cd:
        assert key in YAML_TOP_LEVEL_KEYS or key in extra, \
            f"unknown top-level key in {name}: {key}"
    cd.validate(strict=True)


@pytest.mark.parametrize("name", [
    "single_structure_with_workflow.json",
    "grain_boundary.json",
])
def test_example_json_loads_and_validates(name):
    path = EXAMPLES / name
    if not path.exists():
        pytest.skip(f"example file {name} not present")
    cd = ConceptualDict.from_json(str(path))
    cd.validate(strict=True)


def test_example_yaml_json_equivalent(tmp_path):
    """The YAML and JSON examples should describe the same data."""
    y = EXAMPLES / "single_structure_with_workflow.yaml"
    j = EXAMPLES / "single_structure_with_workflow.json"
    if not (y.exists() and j.exists()):
        pytest.skip("example pair not present")
    cy = ConceptualDict.from_yaml(str(y))
    cj = ConceptualDict.from_json(str(j))
    # at minimum the sample IDs and workflow methods should match
    assert [s.get("id") for s in cy["computational_sample"]] == \
           [s.get("id") for s in cj["computational_sample"]]
    assert [w.get("method") for w in cy["workflow"]] == \
           [w.get("method") for w in cj["workflow"]]


def test_yaml_to_json_to_yaml_roundtrip(tmp_path):
    src = EXAMPLES / "single_structure_with_workflow.yaml"
    if not src.exists():
        pytest.skip("example not present")
    cd = ConceptualDict.from_yaml(str(src))
    j = tmp_path / "out.json"
    cd.to_json(str(j))
    cd2 = ConceptualDict.from_json(str(j))
    y = tmp_path / "out.yaml"
    cd2.to_yaml(str(y))
    cd3 = ConceptualDict.from_yaml(str(y))
    assert cd["computational_sample"] == cd3["computational_sample"]
    assert cd["workflow"] == cd3["workflow"]
