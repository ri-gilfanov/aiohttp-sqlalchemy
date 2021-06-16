from typing import TYPE_CHECKING
import warnings

if TYPE_CHECKING:
    from typing import Any


SA_DEFAULT_KEY = 'sa_main'


def __getattr__(name: str) -> 'Any':
    if name == 'DEFAULT_KEY':
        msg = "'DEFAULT_KEY' has been deprecated, use 'SA_DEFAULT_KEY'"
        warnings.warn(msg, UserWarning, stacklevel=2)
        return SA_DEFAULT_KEY
    raise AttributeError(f"module {__name__} has no attribute {name}")
