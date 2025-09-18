import os
import warnings

from .exceptions import UnstableCoreSchemasWarning

UNSTABLE_ENV_VAR = "ASDF_UNSTABLE_CORE_SCHEMAS"

stable_core_schema_versions = (
    "1.0.0",
    "1.1.0",
    "1.2.0",
    "1.3.0",
    "1.4.0",
    "1.5.0",
    "1.6.0",
)

unstable_core_schema_versions = ("1.7.0",)


_unstable_core_schema_warning = (
    f"{UNSTABLE_ENV_VAR} is enabled and unstable versions of core schemas "
    f"{unstable_core_schema_versions} are in use. Files produced with unstable/development "
    "schemas may later be made invalid due to ongoing schema changes."
)


def get_supported_core_schema_versions():
    if get_unstable_supported():
        return stable_core_schema_versions + unstable_core_schema_versions
    return stable_core_schema_versions


def get_unstable_supported():
    value = os.getenv(UNSTABLE_ENV_VAR)
    if not value:
        return False
    try:
        unstable_supported = bool(int(value))
    except ValueError:
        raise ValueError(f"{UNSTABLE_ENV_VAR} value {value} is not supported, use either 0 or 1")
    if unstable_supported:
        warnings.warn(_unstable_core_schema_warning, UnstableCoreSchemasWarning)
    return unstable_supported
