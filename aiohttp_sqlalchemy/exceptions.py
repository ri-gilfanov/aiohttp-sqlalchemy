class DuplicatedAppKeyError(ValueError):
    def __init__(self, key):
        self.message = f'Duplicated app key `{key}`. Check `engines` argument in `aiohttp_sqlalchemy.setup()` call.'
        super().__init__(self.message)


class DuplicatedRequestKeyError(ValueError):
    def __init__(self, key):
        self.message = f'Duplicated request key `{key}`. Check middlewares and decorators from `aiohttp_sqlalchemy`.'
        super().__init__(self.message)
