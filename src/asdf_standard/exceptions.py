class UnstableCoreSchemasWarning(UserWarning):
    """
    Warning issued when unstable versions of core schemas
    are supported. Writing files with unstable versions is
    highly discouraged and can result in producing files that
    can later be made invalid as schemas evolve.
    """
