# Contributing

### Code Style

This project uses [`black`](https://github.com/psf/black) to automatically
enforce a consistent code style. You can apply `black` and other pre-configured
linters with `tox -e lint`.

This project uses [`flake8`](https://flake8.pycqa.org) and several plugins for
additional checks of documentation style, security issues, good variable
nomenclature, and more (
see [`tox.ini`](tox.ini) for a list of flake8 plugins). You can check if your
code passes `flake8` with `tox -e flake8`.

Each of these checks are run on each commit using GitHub Actions as a continuous
integration service. Passing all of them is required for accepting a
contribution. If you're unsure how to address the feedback from one of these
tools, please say so either in the description of your pull request or in a
comment, and we will help you.

These code style contribution guidelines have been adapted from the
[cthoyt/cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack/blob/main/%7B%7Bcookiecutter.package_name%7D%7D/.github/CODE_OF_CONDUCT.md)
Python package template.
