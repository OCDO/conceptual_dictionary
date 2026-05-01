"""ConceptualDict construction, defaults, and dict semantics."""
import pytest

from conceptual_dictionary import ConceptualDict


def test_default_sections_present():
    cd = ConceptualDict()
    assert cd["computational_sample"] == []
    assert cd["workflow"] == []
    assert cd["operation"] == []
    assert cd["math_operation"] == []


def test_is_dict_subclass():
    cd = ConceptualDict()
    assert isinstance(cd, dict)


def test_construct_from_existing_mapping_merges():
    cd = ConceptualDict({"computational_sample": [{"id": "x"}],
                         "dataset": {"title": "demo"}})
    assert cd["computational_sample"] == [{"id": "x"}]
    assert cd["dataset"] == {"title": "demo"}
    # default empty sections that weren't overridden are still present
    assert cd["workflow"] == []
    assert cd["operation"] == []
    assert cd["math_operation"] == []


def test_arbitrary_top_level_key_accepted():
    cd = ConceptualDict()
    cd["dataset"] = {"title": "x"}
    assert cd["dataset"]["title"] == "x"


def test_generate_id_shape():
    cd = ConceptualDict()
    ident = cd.generate_id()
    assert isinstance(ident, str)
    assert len(ident) == 7
    assert ident.isalnum()


def test_generate_id_custom_length():
    cd = ConceptualDict()
    assert len(cd.generate_id(length=12)) == 12


def test_generate_id_collision_resistance():
    cd = ConceptualDict()
    ids = {cd.generate_id() for _ in range(2000)}
    assert len(ids) == 2000  # no collisions


def test_generate_id_independent_of_random_seed():
    """random.seed must not make IDs deterministic (uses os.urandom)."""
    import random

    cd = ConceptualDict()
    random.seed(42)
    a = cd.generate_id()
    random.seed(42)
    b = cd.generate_id()
    assert a != b
