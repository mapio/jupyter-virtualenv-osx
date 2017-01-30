# Jupyter-virtualenv-osx

Running [Jupyter](https://jupyter.org/) in a
[virtualenv](https://virtualenv.pypa.io/) can be quite cumbersome, expecially on
OS X if, in addition, one needs libraries that require the Frameworks version of
Python, such as, for example, [matplotlib](http://matplotlib.org/). This script
aims to provide a solution to such problem easier (and cleaner) then the the
[known workarounds](http://matplotlib.org/faq/osx_framework.html#osxframework-faq).

First of all, install the [homebrew](http://brew.sh/) version of Python

    brew install python

Then, create the virtual environment you want to execute Jupter from:

    virtualenv my_venv
    source my_venv/bin/activate

or, if using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/):

    mkvirtualenv my_venv

Now add Jupyter and all the required libraries, for instance as

    pip install jupyter matplotlib

Finally, run this scrpit

    python jupyter-virtualenv-osx.py --user --name "My Env"


## How it works

This script will create a kernelspec as the following

    {
      "argv": [
        "/usr/local/bin/python",
        "-m",
        "echo_kernel",
        "-f",
        "{connection_file}"
      ],
      "env": {
        "PYTHONHOME": os.environ['VIRTUAL_ENV']
      },
      "language": "python2",
      "name": name
    }

instructing Jupyter to use the brewed Python and setting up the environment
variable `PYTHONHOME` to be equal to the virtualenv home `$VIRTUAL_ENV`.


##  Using non-virtualenv Jupyter

Even if installing Jupyter in the virtualenv, thus not polluting the system
packages, is a pretty good idea, this script can be used also in case you have a
system-wide installation of Jupyter (or at least of `jupyter-client`), and you
want to install in the virtualenv just the additional libraries. In such a case,
make system packages available in the virtualenv and proceed as before

    mkvirtualenv --system-site-packages my_venv
    pip install matplotlib
    python jupyter-virtualenv-osx.py --user --name "My Env"
