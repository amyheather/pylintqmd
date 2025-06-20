<div align="center">

# pylintqmd

![Code licence](https://img.shields.io/badge/🛡️_Code_licence-MIT-8a00c2?style=for-the-badge&labelColor=gray)
[![ORCID](https://img.shields.io/badge/ORCID_Amy_Heather-0000--0002--6596--3479-A6CE39?style=for-the-badge&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-6596-3479)

</div>

<br>

Package for running pylint on .qmd files.

<br>

## Installation

You can install `pylintqmd` from PyPI:

```
pip install pylintqmd
```

Or, for local development:

```
pip install -e .
```

<br>

## Dependencies

This package uses Flit for packaging and pytest for testing.

A `requirements.txt` file in this repository is provided for development purposes and contains:

```
flit
pytest
-e .
```

To install development dependencies, run:

```
pip install -r requirements.txt
```

<br>

## Usage

To lint file:

```
bash pylintqmd.sh file.qmd
```

To lint all .qmd files in directory

```
bash pylintqmd.sh folder
```

To keep temporary .py files for debugging when lint:
```
KEEP_TEMP_FILES=1 bash pylintqmd.sh file.qmd
```

<br>

## Acknowledgements

Parts of this package were generated or adapted from code provided by [Perplexity](https://www.perplexity.ai/).