#Project File Layout
This project utilizes a src layout, which means the source code cannot be directly run from the root project directory.
There are two primary reasons for this: (1) I'm trying to simulate the end-user environment as closely as possible. By using a src layout, I force myself to install the code as a package in the testing environment just as an end user would. (2) This layout prevents me from accidentally using development code.
This philosophy draws from [Python's documentation on the src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).

#How to Run Development Code
Make sure you're in the project's root directory (not /src but its parent directory). You'll run the following commands to: (1) Create a virtual environment in the root directory and activate it. (2) Install the modules under /src as a package into the virtual envrionment. This packages is defined by the `setup.py` file which should be in the project's root directory. (3) Run the newly installed package.

```shell
$ cd backup-scheduler
$ python -m venv .venv
# Activate your environment with:
#      `source .venv/bin/activate` on Unix/macOS
# or   `.venv\Scripts\activate` on Windows

$ pip install --editable .

# Now you have access to your package as if it was installed in .venv.
# You can import it like you would any other module from a package with the line
# `import abackup` in a python file.

# You can also run the cli command from the shell:
$ abackup
```

These instructions are derived from the ["Development Mode" Python documentation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).