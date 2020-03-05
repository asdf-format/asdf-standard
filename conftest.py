import os

import asdf
from asdf import extension


DIRNAME = os.path.dirname(__file__)

# Check if we're running tests from the current directory.
if DIRNAME == os.path.abspath(os.curdir):
    # Override the ASDF BuiltinExtension so that all ASDF Standard schemas
    # resolve to the ones that are present in this repository, rather than
    # those that are installed with the ASDF python package. This allows for
    # much more direct testing of changes to schemas in this repository.
    local_url_mapping = [
        (
            asdf.constants.STSCI_SCHEMA_URI_BASE,
            asdf.util.filepath_to_url(os.path.join(DIRNAME, "schemas", "stsci.edu")) + "/{url_suffix}.yaml",
        )
    ]

    class LocalBuiltinExtension(extension.BuiltinExtension):
        @property
        def url_mapping(self):
            return local_url_mapping

    exts = extension.default_extensions.extensions
    exts.clear()
    exts.append(LocalBuiltinExtension())
