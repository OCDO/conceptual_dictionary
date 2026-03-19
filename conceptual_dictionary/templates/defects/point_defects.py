# Use exactly ONE of `vacancy`, `substitutional`, or `interstitial` as a key
# directly inside the sample dict (alongside material / simulation_cell etc.).
# `point_defect` is a generic base and rarely needed on its own.

vacancy_template = {
    "concentration": None,  # atomic fraction (float), e.g. 0.004
    "number": None,  # integer count of vacancies, e.g. 1
}

substitutional_template = {
    "concentration": None,  # impurity concentration (atomic fraction), e.g. 0.01
    "number": None,  # integer count of substitutional atoms, e.g. 2
}

interstitial_template = {
    "concentration": None,  # impurity concentration (atomic fraction), e.g. 0.005
    "number": None,  # integer count of interstitial atoms, e.g. 1
}
