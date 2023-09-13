![PyPI - Version](https://img.shields.io/pypi/v/microscopemetrics)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/microscopemetrics)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/MontpellierRessourcesImagerie/microscope-metrics/run_tests_push.yml)
[![GPLv2 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

<img alt="Logo" height="150" src="https://raw.githubusercontent.com/MontpellierRessourcesImagerie/microscope-metrics/main/docs/media/microscopemetrics_logo.png" width="150"/>


# microscope-metrics

_microscope-metrics_ is a Python library to control microscope quality based on standardized samples


## Documentation

By teh time of writing this the documentation is not existing, but you shoudl be able to find it one day following this link
[Documentation](https://github.com/juliomateoslangerak/microscope-metrics/blob/42ff5cba4d4e46310a40f67f3501e43b55eb64d9/docs)
We aim to provide some example code in the future
[examples](https://github.com/juliomateoslangerak/microscope-metrics/blob/d27005964d38c461839ff705652c18358a45f784/docs/examples)
For the time being you can find some examples in the [tests](https://github.com/juliomateoslangerak/microscope-metrics/blob/b2d101745568af294f0b40393aa9ab1fafb3d480/tests)
directory

## Related

microscope-metrics is designed to be used with [microscopemetrics-omero](https://github.com/MontpellierRessourcesImagerie/microscopemetrics-omero.git)
to properly store the results in an OMERO server.
microscope-metrics uses [linkML](https://linkml.github.io/linkml/) to define its data model. This model can be found in
the microscope-metrics [schema](https://github.com/MontpellierRessourcesImagerie/microscopemetrics-schema.git)


## Installation

If you just want to use microscope-metrics you may just install microscope-metrics with pip

```bash
  pip install microscopemetrics
```

For development, we use [poetry](https://python-poetry.org/)
After installing poetry, you can install microscope-metrics running the following command 
in the root directory of the project

```bash
  poetry install
```

## Usage/Examples

```python
# TODO: add some examples
```

## Running Tests

To run tests, use pytest from the root directory of the project

```bash
  pytest 
```

