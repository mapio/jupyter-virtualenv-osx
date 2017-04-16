# Jupyter-virtualenv-osx

Suppose you want run a [Jupyter](https://jupyter.org/) notebook, or console,
with an [IPython](http://ipython.org/) kernel and some additional libraries.
Even if in principle you should be able to install such a software stack (at
least partially) in a [virtualenv](https://virtualenv.pypa.io/), under certain
circumstances this can become quite cumbersome.

In particular this is the case if you use Python 2.7 on OS X and want to add
[matplotlib](http://matplotlib.org/) to your stack: the GUI backend of
matplotlib requires you to use a *Frameworks version* of Python, that is not
what virtualenv provides!

A basic woraround is to run the system (or brewed) Python executable (not the
virtualenv one), but setting the `$PYTHONHOME` environment variable to point to
your virtualenv home, that is setting such variable equal to the value of
`$VIRTUAL_ENV` environment variable. 

The [jupyter-virtualenv-osx](jupyter-virtualenv-osx.py) script automates the
creation of an IPython kernel configuration implementing the above workaround.

## How to use this script

First of all, I suggest to use the [homebrew](http://brew.sh/) version of Python

    brew install python

that (in recent brews) is a Frameworks one, so it will work with the matlab GUI.

Then you have various choices: you can install Jupyter (and IPyhon) system-wide,
or in the virtualenv; then you can add to the virtualenv matplotlib, and the
other libraries you need.

Provided that you have the `jupyter_client` and `ipykernel` packages installed
so that you can import them, and you have activated the virtualenv containing
the libraries you want your IPython kernel to use, just run

    python jupyter-virtualenv-osx.py --user --name my_env

Now if you open a notebook using `my_env` kernel, or launch

    jupyter console --kernel=my_env

and issue the magic command `%matplotlib` you'll see

    Using matplotlib backend: MacOSX

in your output, meaning that the native backend has been selected.

Assuming you want to put everything in a virtualenv (that is the solution I
suggest), the complete set of commands you'll need are

    virtualenv my_venv
    source my_venv/bin/activate

or, if using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/):

    mkvirtualenv my_venv

now install

    pip install jupyter ipykernel matplotlib

finally, run this scrpit

    python jupyter-virtualenv-osx.py --user --name "My Env"


### How it works

This script will create a kerne configuration like the following

    {
      "argv": [
        "/usr/local/bin/python",
        "-m",
        "ipykernel",
        "-f",
        "{connection_file}"
      ],
      "env": {
        "PYTHONHOME": os.environ['VIRTUAL_ENV']
      },
      "language": "python2",
      "display_name": name
    }

instructing Jupyter to use the brewed Python to run the IPython kernel, and
setting the environment variable `$PYTHONHOME` to be equal to the virtualenv
home `$VIRTUAL_ENV`.
