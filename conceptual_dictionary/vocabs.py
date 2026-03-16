# atomrdf/datamodels/workflow/method.py  (method_map)
METHOD = frozenset(
    {
        "MolecularDynamics",
        "MolecularStatics",
        "DensityFunctionalTheory",
    }
)

# atomrdf/datamodels/workflow/algorithm.py  (algorithm_map)
# parser alias: "UniaxialTension" -> "TensileTest"  (io/workflow_parser.py)
ALGORITHM = frozenset(
    {
        "EquationOfStateFit",
        "QuasiHarmonicApproximation",
        "ThermodynamicIntegration",
        "ANNNIModel",
        "TensileTest",
        "CompressionTest",
        # legacy parser alias accepted by WorkflowParser
        "UniaxialTension",
    }
)

# atomrdf/datamodels/workflow/dof.py  (dof_map)
DEGREES_OF_FREEDOM = frozenset(
    {
        "AtomicPositionRelaxation",
        "CellVolumeRelaxation",
        "CellShapeRelaxation",
    }
)

# atomrdf/datamodels/workflow/ensemble.py  (ensemble_map)
THERMODYNAMIC_ENSEMBLE = frozenset(
    {
        "CanonicalEnsemble",
        "MicrocanonicalEnsemble",
        "IsothermalIsobaricEnsemble",
        "IsoenthalpicIsobaricEnsemble",
        "GrandCanonicalEnsemble",
    }
)

# atomrdf/datamodels/workflow/potential.py  (potential_map)
# Canonical names + all short aliases that atomRDF accepts without error.
POTENTIAL_TYPE = frozenset(
    {
        # canonical
        "InteratomicPotential",
        "EmbeddedAtomModel",
        "ModifiedEmbeddedAtomModel",
        "LennardJonesPotential",
        "MachineLearningPotential",
        # short aliases (case-sensitive as in potential_map)
        "EAM",
        "eam",
        "eam/alloy",
        "eam/fs",  # LAMMPS pair_style strings, used in practice
        "MEAM",
        "meam",
        "ACE",
        "pace",
        "LJ",
        "lj",
        "HDNNP",
        "hdnnp",
        "grace",
        "GRACE",  # GRACE machine learning potential
    }
)

# atomrdf/datamodels/workflow/xcfunctional.py  (xc_map)
# Unknown strings fall back to a generic XCFunctional node (no error in atomRDF),
# but listing known values makes typos visible.
XC_FUNCTIONAL = frozenset(
    {
        "LDA",
        "GGA",
        "PBE",  # alias → GGA
    }
)

# atomrdf/io/workflow_parser.py  OPERATION_MAP
OPERATION_METHOD = frozenset(
    {
        "DeleteAtom",
        "SubstituteAtom",
        "AddAtom",
        "Rotate",
        "Rotation",  # alias accepted by parser
        "Translate",
        "Translation",  # alias accepted by parser
        "Shear",
    }
)

# atomrdf/datamodels/workflow/math_operations.py  MATH_OPERATION_MAP
MATH_OPERATION_TYPE = frozenset(
    {
        "Subtraction",
        "Addition",
        "Multiplication",
        "Division",
        "Exponentiation",
    }
)

# atomrdf/datamodels/defects/grainboundary.py
# These are the YAML key names that atomRDF maps to PLDO.* RDF types.
GRAIN_BOUNDARY_TYPE = frozenset(
    {
        "grain_boundary",
        "tilt_grain_boundary",
        "twist_grain_boundary",
        "symmetric_tilt_grain_boundary",
        "mixed_grain_boundary",
    }
)

# atomrdf/io/workflow_parser.py  (top-level section keys read by parse())
YAML_TOP_LEVEL_KEYS = frozenset(
    {
        "computational_sample",
        "workflow",
        "operation",
        "activity",  # legacy alias for "operation"
        "math_operation",
    }
)

# -------------------------------------------------------------------
# Convenience dict: field_path  →  (frozenset of allowed values, scope)
# "scope" is just a human-readable note for error messages.
# -------------------------------------------------------------------
CONTROLLED_VALUES = {
    "workflow.method": (METHOD, "workflow entry"),
    "workflow.algorithm": (ALGORITHM, "workflow entry"),
    "workflow.degrees_of_freedom": (DEGREES_OF_FREEDOM, "workflow entry (each item)"),
    "workflow.thermodynamic_ensemble": (THERMODYNAMIC_ENSEMBLE, "workflow entry"),
    "workflow.potential_type": (POTENTIAL_TYPE, "workflow.interatomic_potential"),
    "workflow.xc_functional": (XC_FUNCTIONAL, "workflow entry"),
    "operation.method": (OPERATION_METHOD, "operation entry"),
    "math_operation.type": (MATH_OPERATION_TYPE, "math_operation entry"),
}
