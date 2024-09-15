from __future__ import annotations


class AbstractDuplicateKeyError(ValueError):
    message: str


class DuplicateAppKeyError(AbstractDuplicateKeyError):
    def __init__(self, key: str) -> None:
        msg = (
            f"Duplicated app key `{key}`. Check `bindings` argument "
            f"in `aiohttp_sqlalchemy.setup()` call."
        )
        super().__init__(msg)


class DuplicateRequestKeyError(AbstractDuplicateKeyError):
    def __init__(self, key: str) -> None:
        msg = (
            f"Duplicated request key `{key}`. Check middlewares and "
            f"decorators from `aiohttp_sqlalchemy`."
        )
        super().__init__(msg)
