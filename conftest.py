import os

# Only add this plugin definition when not being run as part of a submodule
if os.path.dirname(__file__) == os.path.abspath(os.curdir):
    pytest_plugins = [
        'asdf.tests.schema_tester'
    ]
