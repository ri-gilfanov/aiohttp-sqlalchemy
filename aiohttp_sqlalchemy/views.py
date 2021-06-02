from abc import ABCMeta
from aiohttp.abc import AbstractView
from aiohttp.web import View
from typing import TYPE_CHECKING

from aiohttp_sqlalchemy.constants import DEFAULT_KEY

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from typing import Any


class SAAbstractView(AbstractView, metaclass=ABCMeta):
    """ SQLAlchemy view based on aiohttp.abc.AbstractView """

    def sa_session(self, key: str = DEFAULT_KEY) -> 'AsyncSession':
        return self.request[key]


class SAOneModelMixin(SAAbstractView, metaclass=ABCMeta):
    sa_model: 'Any'  # Not all developers use declarative mapping


class SABaseView(View, SAAbstractView):
    """ Simple SQLAlchemy view based on aiohttp.web.View """


class SAView(View, SAOneModelMixin):
    """ One model SQLAlchemy view """
