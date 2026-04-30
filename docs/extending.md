# Extending

In case of bugs and feature improvements, you are welcome to create a new
issue on the [GitHub repo](https://github.com/OCDO/conceptual_dictionary).
You are also welcome to fix a bug or implement a feature.

`conceptual_dictionary` welcomes contribution and extension. Rather than
local modifications, we ask that changes be submitted through a pull request
so the package can be continuously improved.

## Reporting and fixing bugs

Bugs can be reported on the
[issues page](https://github.com/OCDO/conceptual_dictionary/issues). Once a
bug is reported, the status can also be tracked there. You are very welcome
to fix any existing bug.

## New features

Feature ideas can be submitted through the same
[issues page](https://github.com/OCDO/conceptual_dictionary/issues). The more
detail you can provide about the feature, the better. You can also work on
feature requests already open on the issues page.

### Setting up a local environment

1. Fork `conceptual_dictionary` (a tutorial on forking is
   [here](https://help.github.com/en/articles/fork-a-repo)). After forking,
   clone the repository locally.
2. Create a virtual environment to test new features. See
   [this link](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
   for help managing environments.
3. Create a feature branch:
   ```bash
   git checkout -b new_feature
   ```
4. Implement the feature.
5. Reinstall in editable mode and run the tests:
   ```bash
   pip install -e .
   pip install pytest
   pytest tests/ -q
   ```
6. If the new feature is not covered by existing tests, please add one in
   `tests/`. The package uses [pytest](http://doc.pytest.org).
7. Add docstrings (numpy style) for any new public function or class.
8. Update / add documentation pages where relevant.
9. Submit a pull request through GitHub. Once submitted, automated tests will
   run; if they pass and review is approved, your feature will be merged and
   credited.

## Adding new controlled-vocabulary values

When atomRDF gains a new method, algorithm or potential type:

1. Add the new string to the appropriate `frozenset` in
   [`conceptual_dictionary/vocabs.py`](https://github.com/OCDO/conceptual_dictionary/blob/main/conceptual_dictionary/vocabs.py).
2. If you introduced a new top-level field, also add an entry to
   `CONTROLLED_VALUES` so it is picked up by
   [`ConceptualDict.validate`](validation.md).
3. Update [](vocabularies.md).
4. Add a test in `tests/test_validate.py`.

If you have any trouble with these steps, please
[open an issue](https://github.com/OCDO/conceptual_dictionary/issues) — we
are happy to help.
