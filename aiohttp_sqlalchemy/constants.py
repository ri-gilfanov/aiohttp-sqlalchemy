import warnings


SA_DEFAULT_KEY = 'sa_main'


def __getattr__(name):
    if name == 'DEFAULT_KEY':
        msg = "'DEFAULT_KEY' has been deprecated, use 'SA_DEFAULT_KEY'"
        warnings.warn(msg, UserWarning, stacklevel=2)
        return SA_DEFAULT_KEY
    raise AttributeError(f"module {__name__} has no attribute {name}")
