from abc import ABCMeta
from typing import Any, Optional

from aiohttp.abc import AbstractView
from aiohttp.web import View
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY


class SAAbstractView(AbstractView, metaclass=ABCMeta):
    """Simple SQLAlchemy view based on aiohttp.abc.AbstractView."""
    sa_session_key: str = SA_DEFAULT_KEY

    def sa_session(self, key: Optional[str] = None) -> AsyncSession:
        session = self.request.get(key or self.sa_session_key)
        if isinstance(session, AsyncSession):
            return session
        raise TypeError(f"{session} is not {AsyncSession}")


class SAOneModelMixin(SAAbstractView, metaclass=ABCMeta):
    """One model SQLAlchemy view based on aiohttp.abc.AbstractView."""
    sa_model: Any  # Not all developers use declarative mapping


class SABaseView(View, SAAbstractView):
    """Simple SQLAlchemy view based on aiohttp.web.View."""


class SAView(View, SAOneModelMixin):
    """One model SQLAlchemy view based on aiohttp.web.View."""
