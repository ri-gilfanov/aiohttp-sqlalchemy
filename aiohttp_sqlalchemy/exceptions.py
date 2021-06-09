class AbstractDuplicateKeyError(ValueError):
    message: str


class DuplicateAppKeyError(AbstractDuplicateKeyError):
    def __init__(self, key: str):
        self.message = f'Duplicated app key `{key}`. Check `bindings` ' \
                       f' argument in `aiohttp_sqlalchemy.setup()` call.'
        super().__init__(self.message)


class DuplicateRequestKeyError(AbstractDuplicateKeyError):
    def __init__(self, key: str):
        self.message = f'Duplicated request key `{key}`. Check middlewares ' \
                       f'and decorators from `aiohttp_sqlalchemy`.'
        super().__init__(self.message)
