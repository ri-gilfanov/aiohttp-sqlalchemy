from abc import ABCMeta
from typing import Any, Optional

from aiohttp.abc import AbstractView
from aiohttp.web import View
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.utils import sa_session


class SAMixin(AbstractView, metaclass=ABCMeta):
    """SQLAlchemy view mixin based ``aiohttp.abc.AbstractView``."""

    sa_session_key: str = SA_DEFAULT_KEY

    def sa_session(self, key: Optional[str] = None) -> AsyncSession:
        """Return ``AsyncSession`` instance."""
        return sa_session(self.request, key or self.sa_session_key)


SAAbstractView = SAMixin  # synonym


class SAModelMixin(SAMixin, metaclass=ABCMeta):
    """SQLAlchemy single model view mixin based ``aiohttp.abc.AbstractView``."""

    sa_model: Any  # Not all developers use declarative mapping


SAOneModelMixin = SAModelMixin  # synonym


class SABaseView(View, SAMixin):
    """SQLAlchemy class based view."""


class SAView(View, SAModelMixin):
    """SQLAlchemy single model class based view."""
