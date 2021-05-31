from typing import TYPE_CHECKING
from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Any


class SAViewMixin:
    """ SQLAlchemy class based view mixin. """
    request: 'Request'
    sa_model: 'Any'  # Not all developers use declarative mapping

    @property
    def sa_main_session(self) -> 'AsyncSession':
        return self.request[DEFAULT_KEY]
