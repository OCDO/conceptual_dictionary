# Installation

`conceptual_dictionary` is a pure-Python package with two runtime
dependencies: [PyYAML](https://pyyaml.org/) and [NumPy](https://numpy.org/).
It runs on Linux, macOS and Windows on Python 3.9 or newer.

````{tab-set}
```{tab-item} pip
`pip install conceptual-dictionary`
```

```{tab-item} conda
`conda install -c conda-forge conceptual-dictionary`

(coming with the next release; until then please use `pip`.)
```

```{tab-item} from source
We recommend creating a virtual environment for development. To see how to
install conda, see [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

Clone the repository:

`git clone https://github.com/OCDO/conceptual_dictionary.git`

Then install in editable mode:

`cd conceptual_dictionary`
`pip install -e .`

To run the test suite:

`pip install pytest`
`pytest tests/ -q`
```
````

## Verify

```python
import conceptual_dictionary as cd
print(cd.__all__)
```

If the import succeeds and prints the list of public names, you are ready to
move on to the [quickstart](quickstart.md).
