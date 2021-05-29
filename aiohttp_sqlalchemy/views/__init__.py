from aiohttp.web import View
from typing import TYPE_CHECKING
from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncEngine


class SAViewMixin:
    """ SQLAlchemy class based view mixin. """
    request: 'Request'

    @property
    def sa_main_session(self) -> 'AsyncEngine':
        return self.request[DEFAULT_KEY]


class SAView(View, SAViewMixin):
    """ SQLAlchemy class based view. """
    pass
