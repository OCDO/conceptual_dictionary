"""YAML / JSON round-trip and numpy cleanup."""
import json
import copy

import numpy as np
import pytest
import yaml

from conceptual_dictionary import (
    ConceptualDict,
    sample_template,
    workflow_template,
    property_template,
)


def _build_populated_cd():
    cd = ConceptualDict()
    s = copy.deepcopy(sample_template)
    s["id"] = "Al_fcc"
    s["material"]["element_ratio"] = {"Al": 1.0}
    s["simulation_cell"]["volume"]["value"] = 65.5
    cd["computational_sample"].append(s)

    wf = copy.deepcopy(workflow_template)
    wf["method"] = "MolecularStatics"
    wf["interatomic_potential"] = {"potential_type": "eam/alloy", "uri": "x"}
    wf["input_sample"] = ["Al_fcc"]
    wf["output_sample"] = ["Al_fcc"]

    p = copy.deepcopy(property_template)
    p.update({"label": "EquilibriumEnergy", "value": -3.36, "unit": "EV",
              "associate_to_sample": ["Al_fcc"]})
    wf["calculated_property"] = [p]
    cd["workflow"].append(wf)
    return cd


def test_yaml_roundtrip(tmp_path):
    cd = _build_populated_cd()
    path = tmp_path / "out.yaml"
    cd.to_yaml(str(path))
    loaded = ConceptualDict.from_yaml(str(path))
    assert loaded["computational_sample"][0]["id"] == "Al_fcc"
    assert loaded["workflow"][0]["method"] == "MolecularStatics"
    assert loaded["workflow"][0]["calculated_property"][0]["value"] == -3.36


def test_json_roundtrip(tmp_path):
    cd = _build_populated_cd()
    path = tmp_path / "out.json"
    cd.to_json(str(path))
    loaded = ConceptualDict.from_json(str(path))
    assert loaded["computational_sample"][0]["material"]["element_ratio"] == {"Al": 1.0}
    assert loaded["workflow"][0]["interatomic_potential"]["potential_type"] == "eam/alloy"


def test_yaml_partial_file_loads(tmp_path):
    """Partial files (missing some top-level keys) should load with empty defaults."""
    path = tmp_path / "partial.yaml"
    path.write_text("computational_sample:\n  - id: foo\n")
    loaded = ConceptualDict.from_yaml(str(path))
    assert loaded["computational_sample"] == [{"id": "foo"}]
    assert loaded["workflow"] == []
    assert loaded["operation"] == []
    assert loaded["math_operation"] == []


def test_numpy_arrays_serialized_as_lists(tmp_path):
    cd = ConceptualDict()
    cd["computational_sample"].append({
        "id": "x",
        "atom_attribute": {
            "position": np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]),
            "species": np.array(["Al", "Al"]),
        },
    })
    yaml_path = tmp_path / "np.yaml"
    cd.to_yaml(str(yaml_path))
    raw = yaml.safe_load(yaml_path.read_text())
    pos = raw["computational_sample"][0]["atom_attribute"]["position"]
    assert isinstance(pos, list) and pos[0] == [0.0, 0.0, 0.0]


def test_numpy_scalars_serialized_as_native(tmp_path):
    cd = ConceptualDict()
    cd["computational_sample"].append({
        "id": "x",
        "value_f": np.float64(1.5),
        "value_i": np.int64(42),
        "value_b": np.bool_(True),
    })
    json_path = tmp_path / "np.json"
    cd.to_json(str(json_path))
    raw = json.loads(json_path.read_text())
    sample = raw["computational_sample"][0]
    assert sample["value_f"] == 1.5 and isinstance(sample["value_f"], float)
    assert sample["value_i"] == 42 and isinstance(sample["value_i"], int)
    assert sample["value_b"] is True


def test_to_json_indent_and_sort(tmp_path):
    cd = ConceptualDict()
    cd["computational_sample"].append({"b": 1, "a": 2})
    p = tmp_path / "out.json"
    cd.to_json(str(p), sort_keys=True, indent=4)
    text = p.read_text()
    assert "    " in text  # indent applied
    # within the sample dict, a should appear before b
    sample_str = text[text.index("{", text.index("computational_sample")):]
    assert sample_str.index('"a"') < sample_str.index('"b"')


def test_unknown_object_falls_back_to_str(tmp_path):
    class Foo:
        def __str__(self):
            return "foo-repr"

    cd = ConceptualDict()
    cd["computational_sample"].append({"id": "x", "obj": Foo()})
    p = tmp_path / "out.json"
    cd.to_json(str(p))
    raw = json.loads(p.read_text())
    assert raw["computational_sample"][0]["obj"] == "foo-repr"
