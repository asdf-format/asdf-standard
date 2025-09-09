import os
import warnings

from .exceptions import DevCoreSchemasWarning

DEV_ENV_VAR = "ASDF_DEV_CORE_SCHEMAS"

stable_core_schema_versions = (
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "1.3.0",
    "1.4.0",
    "1.5.0",
    "1.6.0",
)

dev_core_schema_versions = ("1.7.0",)


_dev_core_schema_warning = (
    f"{DEV_ENV_VAR} is enabled and development versions of core schemas "
    f"{dev_core_schema_versions} are in use. Files produced with development "
    "schemas may later be made invalid due to ongoing schema changes."
)


def get_supported_core_schema_versions():
    if get_dev_supported():
        warnings.warn(_dev_core_schema_warning, DevCoreSchemasWarning)
        return stable_core_schema_versions + dev_core_schema_versions
    return stable_core_schema_versions


def get_dev_supported():
    value = os.getenv(DEV_ENV_VAR)
    if not value:
        return False
    try:
        return bool(int(value))
    except ValueError:
        raise ValueError(f"{DEV_ENV_VAR} value {value} is not supported, use either 0 or 1")
