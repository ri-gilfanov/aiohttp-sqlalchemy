from abc import ABCMeta
from aiohttp.abc import AbstractView
from aiohttp.web import View
from sqlalchemy import delete, insert, join, select, update
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql import Delete, Insert, Join, Select, Update
    from typing import Any


class SAViewMixin:
    """ SQLAlchemy class based view mixin. """
    request: 'Request'

    @property
    def sa_main_session(self) -> 'AsyncSession':
        return self.request[DEFAULT_KEY]


class SAOneModelMixin(SAViewMixin):
    sa_model: 'Any'  # Not all developers use declarative mapping


class AbstractSAView(AbstractView, SAViewMixin, metaclass=ABCMeta):
    """ SQLAlchemy view based on aiohttp.abc.AbstractView """


class SAView(View, SAViewMixin):
    """ SQLAlchemy view based on aiohttp.web.View """
