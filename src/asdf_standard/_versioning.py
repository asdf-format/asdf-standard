import os

DEV_ENV_VAR = "ASDF_DEV_CORE_SCHEMAS"


def get_dev_supported():
    value = os.getenv(DEV_ENV_VAR)
    if not value:
        return False
    try:
        return bool(int(value))
    except ValueError:
        raise ValueError(f"{DEV_ENV_VAR} value {value} is not supported, use either 0 or 1")
