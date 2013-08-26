# pyquality

## Introduction

`pyquality` is a tool to measure Python code quality with a focus on **rich
reports** that take into account the **history of the code**.

Still in an early development stage, `pyquality` analyses the conformity to
PEP8 standards throughout a project's history and generates a full report
including a video showing the evolution of the code.

We aim to make it easy to include new analysis and reports, and also support
different version control systems (only Git is supported for now).


## Installation

To install a stable version, install it directly from
[PyPI](http://pypi.python.org/) using `pip`:

    pip install pyquality


You can also clone pyquality's repository and install our `develop` branch:

    git clone git@github.com:NAMD/pyquality.git
    cd pyquality
    python setup.py install


## Using it

Once you've installed `pyquality`, a command called `pyquality` will be
available in your system/virtualenv. To create a report based on a existing Git
repository, just execute:

    pyquality /path/to/Git/repository

If do you want to create a report based on a remote Git repository, just
replace the path with the URL, for example, to run `pyquality` against its own
repository, execute:

    pyquality git@github.com:NAMD/pyquality.py


## Contributing

`pyquality` is on early stage of development but we have good plans for this
tool! You can contribute by suggesting new features, implementing it, reporting
bugs or fixing it.

If you don't have ideas of new features and haven't found a bug, you can just
look for an issue you can solve on our
[issue tracker](https://github.com/NAMD/pyquality/issues).

### Project guidelines

- We use [nvie's git-flow](http://nvie.com/git-model/);
- We use [semantic versioning](http://semver.org/);
- We love automated tests and [test-driven
  development](http://en.wikipedia.org/wiki/Test-driven_development), but
  there's a lack of tests in this project - we still need help to increase the
  test coverage.
