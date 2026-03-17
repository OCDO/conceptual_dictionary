import warnings
import yaml
import json
from typing import Any, Dict, List
import numpy as np
import string
import random

from conceptual_dictionary.vocabs import CONTROLLED_VALUES


class ConceptualDict(dict):
    def __init__(self, *args, **kwargs):
        data = {
            "computational_sample": [],
            "workflow": [],
            "operation": [],
            "math_operation": [],
        }
        super().__init__(data, *args, **kwargs)

    def generate_id(self, length=7):
        """Generate a random alphanumeric ID of given length.

        Uses ``os.urandom`` rather than Python's ``random`` module so that
        third-party libraries that call ``random.seed()`` (e.g. PyIron/LAMMPS
        wrappers) cannot cause ID collisions across iterations.
        """
        import os
        chars = string.ascii_letters + string.digits
        return "".join(chars[b % 62] for b in os.urandom(length))

    @staticmethod
    def _clean_data(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: ConceptualDict._clean_data(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ConceptualDict._clean_data(v) for v in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif obj is None or isinstance(obj, (str, float, int)):
            return obj
        else:
            return str(obj)

    # --------------------
    # YAML I/O
    # --------------------
    def to_yaml(self, filepath: str, sort_keys: bool = False) -> None:
        clean_dict = ConceptualDict._clean_data(dict(self))
        with open(filepath, "w") as f:
            yaml.safe_dump(clean_dict, f, sort_keys=sort_keys, allow_unicode=True)

    @classmethod
    def from_yaml(cls, filepath: str) -> "ConceptualDict":
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        kg = cls()
        kg.update(data)
        return kg

    # --------------------
    # JSON I/O
    # --------------------
    def to_json(self, filepath: str, sort_keys: bool = False, indent: int = 2) -> None:
        clean_dict = ConceptualDict._clean_data(dict(self))
        with open(filepath, "w") as f:
            json.dump(
                clean_dict, f, sort_keys=sort_keys, indent=indent, ensure_ascii=False
            )

    @classmethod
    def from_json(cls, filepath: str) -> "ConceptualDict":
        with open(filepath, "r") as f:
            data = json.load(f)
        kg = cls()
        kg.update(data)
        return kg

    # --------------------
    # Validation
    # --------------------
    def validate(self, strict: bool = False) -> List[dict]:
        """Check all entries against controlled vocabularies sourced from atomRDF.

        Parameters
        ----------
        strict : bool
            If False (default), emit ``warnings.warn`` for each violation and
            return the full list.  If True, raise ``ValueError`` on the first
            violation — useful in CI / test contexts.

        Returns
        -------
        list[dict]
            Each item has keys ``section``, ``index``, ``field``, ``value``,
            ``allowed`` so callers can inspect violations programmatically.
        """
        violations: List[dict] = []

        def _check(section: str, idx: int, field: str, value, allowed: frozenset):
            if value is None:
                return
            values = value if isinstance(value, list) else [value]
            for v in values:
                if v not in allowed:
                    msg = (
                        f"[{section}][{idx}] '{field}' has invalid value '{v}'. "
                        f"Allowed: {sorted(allowed)}"
                    )
                    violations.append(
                        dict(
                            section=section,
                            index=idx,
                            field=field,
                            value=v,
                            allowed=allowed,
                        )
                    )
                    if strict:
                        raise ValueError(msg)
                    warnings.warn(msg, UserWarning, stacklevel=2)

        for i, wf in enumerate(self.get("workflow", [])):
            _check(
                "workflow",
                i,
                "method",
                wf.get("method"),
                CONTROLLED_VALUES["workflow.method"][0],
            )
            _check(
                "workflow",
                i,
                "algorithm",
                wf.get("algorithm"),
                CONTROLLED_VALUES["workflow.algorithm"][0],
            )
            _check(
                "workflow",
                i,
                "degrees_of_freedom",
                wf.get("degrees_of_freedom"),
                CONTROLLED_VALUES["workflow.degrees_of_freedom"][0],
            )
            _check(
                "workflow",
                i,
                "thermodynamic_ensemble",
                wf.get("thermodynamic_ensemble"),
                CONTROLLED_VALUES["workflow.thermodynamic_ensemble"][0],
            )
            _check(
                "workflow",
                i,
                "xc_functional",
                wf.get("xc_functional"),
                CONTROLLED_VALUES["workflow.xc_functional"][0],
            )
            pot = wf.get("interatomic_potential")
            if isinstance(pot, dict):
                _check(
                    "workflow",
                    i,
                    "potential_type",
                    pot.get("potential_type"),
                    CONTROLLED_VALUES["workflow.potential_type"][0],
                )

        for i, op in enumerate(self.get("operation", [])):
            _check(
                "operation",
                i,
                "method",
                op.get("method"),
                CONTROLLED_VALUES["operation.method"][0],
            )

        for i, mo in enumerate(self.get("math_operation", [])):
            _check(
                "math_operation",
                i,
                "type",
                mo.get("type"),
                CONTROLLED_VALUES["math_operation.type"][0],
            )

        return violations
