class DevCoreSchemasWarning(UserWarning):
    """
    Warning issued when development versions of core schemas
    are supported. Writing files with development versions is
    highly discouraged and can result in producing files that
    can later be made invalid as development schemas evolve.
    """
