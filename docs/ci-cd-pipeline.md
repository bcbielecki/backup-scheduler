# Git Repo CI/CD
This repo utilizes GitHub Actions to package, lint, and test (based on unittests) commits on a variety of Python versions and operating systems.
The pipeline is based on this [GitHub Action Python documentation](https://docs.github.com/en/actions/tutorials/build-and-test-code/python#using-a-python-workflow-template).

The actions are stored in .yaml files under the repo directory [./.github/workflows/](https://github.com/bcbielecki/backup-scheduler/tree/main/.github/workflows)

The syntax for workflow .yaml files can be found on this [GitHub reference page](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

Although the officially supported platforms are fewer, we currently test on Ubuntu, Windows, and Mac-OS for Python Versions 3.10-3.13


# Test Coverage
Ensure all tests are under the /test directory and end with `*_tests.py` so they are picked up by the CI/CD script.