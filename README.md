![PyPI - Version](https://img.shields.io/pypi/v/microscopemetrics)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/microscopemetrics)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/MontpellierRessourcesImagerie/microscope-metrics/run_tests_push.yml)
[![GPLv2 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

<img alt="Logo" height="150" src="https://raw.githubusercontent.com/MontpellierRessourcesImagerie/microscope-metrics/main/docs/media/microscopemetrics_logo.png" width="150"/>


# microscope-metrics

_microscope-metrics_ is a Python library to control microscope quality based on standardized samples


## Documentation

You may find documentation the [Documentation](https://github.com/juliomateoslangerak/microscope-metrics/blob/42ff5cba4d4e46310a40f67f3501e43b55eb64d9/docs) pages.

We aim to provide some example code in the future
[examples](https://github.com/juliomateoslangerak/microscope-metrics/blob/d27005964d38c461839ff705652c18358a45f784/docs/examples)
For the time being please refer to the [tests](https://github.com/juliomateoslangerak/microscope-metrics/blob/b2d101745568af294f0b40393aa9ab1fafb3d480/tests)
directory to find some example code

## Related to

microscope-metrics is designed to be used with [microscopemetrics-omero](https://github.com/MontpellierRessourcesImagerie/microscopemetrics-omero.git)
to store the results in an OMERO server.
The measurements made by micrsocope-metrics are backed up by a model that can be found in the 
[microscopemetrics-schema](https://github.com/MontpellierRessourcesImagerie/microscopemetrics-schema.git) repository. The model is also accessible through the 
[schema website](https://montpellierressourcesimagerie.github.io/microscopemetrics-schema/)

## Installation

If you just want to use microscope-metrics you may just install microscope-metrics with pip

```bash
  pip install microscopemetrics
```

For development, we use [poetry](https://python-poetry.org/)
After [installing poetry](https://python-poetry.org/docs/#installation), you can install microscope-metrics running the following command 
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

