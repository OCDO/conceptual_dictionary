import warnings
import yaml
import json
from typing import Any, Dict, List
import numpy as np
import string
import random

from conceptual_dictionary.vocabs import CONTROLLED_VALUES


class ConceptualDict(dict):
    """A ``dict`` subclass pre-populated with the top-level sections that
    atomRDF's :class:`~atomrdf.io.workflow_parser.WorkflowParser` consumes.

    On construction the instance contains four empty lists::

        {
            "computational_sample": [],
            "workflow": [],
            "operation": [],
            "math_operation": [],
        }

    Arbitrary additional top-level keys (e.g. ``"dataset"``) may be added at
    any time via normal item assignment.  All standard ``dict`` methods
    (``update``, ``get``, ``setdefault``, iteration, ...) are inherited.

    Parameters
    ----------
    *args, **kwargs
        Forwarded to ``dict.__init__`` *after* the default sections are
        inserted, so passing a mapping merges it on top of the defaults::

            ConceptualDict({"computational_sample": [sample_dict]})

    Notes
    -----
    Serialization (:meth:`to_yaml`, :meth:`to_json`) automatically converts
    numpy scalars/arrays to native Python types, so values written by
    ASE / pyiron / LAMMPS callers can be stored without manual cleanup.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        # default empty top-level sections
        super().update({
            "computational_sample": [],
            "workflow": [],
            "operation": [],
            "math_operation": [],
        })
        # merge any user-provided mapping(s) on top of the defaults
        if args or kwargs:
            super().update(*args, **kwargs)

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
        """Recursively convert numpy / non-JSON types to plain Python.

        Used internally by :meth:`to_yaml` and :meth:`to_json` so callers can
        store numpy arrays, numpy scalars and arbitrary objects without
        worrying about serializer compatibility.  Unknown objects fall back
        to ``str(obj)``.
        """
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
        """Write the dictionary to ``filepath`` as YAML.

        Parameters
        ----------
        filepath : str
            Output path.  Existing files are overwritten.
        sort_keys : bool, default False
            Forwarded to :func:`yaml.safe_dump`.  The default preserves the
            insertion order of the templates, which is friendlier for diffs
            and human inspection.
        """
        clean_dict = ConceptualDict._clean_data(dict(self))
        with open(filepath, "w") as f:
            yaml.safe_dump(clean_dict, f, sort_keys=sort_keys, allow_unicode=True)

    @classmethod
    def from_yaml(cls, filepath: str) -> "ConceptualDict":
        """Load a YAML file into a new :class:`ConceptualDict`.

        Top-level keys present in the file are merged on top of the default
        empty sections, so partial files (e.g. only ``computational_sample``)
        are accepted.
        """
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        kg = cls()
        kg.update(data)
        return kg

    # --------------------
    # JSON I/O
    # --------------------
    def to_json(self, filepath: str, sort_keys: bool = False, indent: int = 2) -> None:
        """Write the dictionary to ``filepath`` as JSON.

        Parameters
        ----------
        filepath : str
            Output path.  Existing files are overwritten.
        sort_keys : bool, default False
            Forwarded to :func:`json.dump`.
        indent : int, default 2
            Forwarded to :func:`json.dump`.  Use ``None`` for a compact
            single-line representation.
        """
        clean_dict = ConceptualDict._clean_data(dict(self))
        with open(filepath, "w") as f:
            json.dump(
                clean_dict, f, sort_keys=sort_keys, indent=indent, ensure_ascii=False
            )

    @classmethod
    def from_json(cls, filepath: str) -> "ConceptualDict":
        """Load a JSON file into a new :class:`ConceptualDict`.

        Top-level keys present in the file are merged on top of the default
        empty sections, so partial files are accepted.
        """
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
