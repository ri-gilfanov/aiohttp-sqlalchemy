from abc import ABCMeta
from typing import Any, Optional

from aiohttp.web import View
from aiohttp_things.views import ContextMixin, InstanceMixin, PrimaryKeyMixin
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.utils import get_session


class SAMixin(ContextMixin, metaclass=ABCMeta):
    """SQLAlchemy class based view mixin."""

    sa_session_key: str = SA_DEFAULT_KEY

    def sa_session(self, key: Optional[str] = None) -> AsyncSession:
        """Return `AsyncSession` instance.

        :param key: key of SQLAlchemy binding.
        """
        return get_session(self.request, key or self.sa_session_key)


class SAModelMixin(SAMixin, metaclass=ABCMeta):
    """SQLAlchemy single model class based view mixin."""

    sa_model: Any = None  # Not all developers use declarative mapping


class SAInstanceMixin(
    InstanceMixin,
    PrimaryKeyMixin,
    SAModelMixin,
    metaclass=ABCMeta,
):
    """
    SQLAlchemy single instance class based view mixin.

    :param sa_pk_attr: primary key column or hybrid attribute.
    """
    sa_pk_attr: Any = getattr(SAModelMixin.sa_model, 'pk', None)


class SABaseView(View, SAMixin):
    """SQLAlchemy class based view."""


class SAModelView(View, SAModelMixin):
    """SQLAlchemy single model class based view."""


class SAInstanceView(View, SAInstanceMixin, metaclass=ABCMeta):
    """SQLAlchemy single instance class based view."""


# Synonyms
SAAbstractView = SAMixin
SAItemMixin = SAInstanceMixin
SAItemView = SAInstanceView
SAOneModelMixin = SAModelMixin
SAView = SAModelView
