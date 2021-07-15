from abc import ABCMeta
from typing import Any, List, Optional

import aiohttp_things as ahth
from aiohttp.web import View
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Select, Update

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.utils import get_session


class SAMixin(ahth.ContextMixin, metaclass=ABCMeta):
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


class SAModelDeleteMixin(SAModelMixin):
    def get_sa_delete_stmt(self, model: Any = None) -> Delete:
        return delete(model or self.sa_model)


class SAModelEditMixin(SAModelMixin):
    def get_sa_update_stmt(self, model: Any = None) -> Update:
        return update(model or self.sa_model)


class SAModelViewMixin(SAModelMixin):
    def get_sa_select_stmt(self, model: Any = None) -> Select:
        return select(model or self.sa_model)


class SAPrimaryKeyMixin(ahth.PrimaryKeyMixin, SAModelMixin, metaclass=ABCMeta):
    """
    Primary key mixin for deleting, editing and viewing a single instance
    by primary key.

    :param sa_pk_attr: primary key column or hybrid attribute.
    """
    sa_pk_attr: Any = getattr(SAModelMixin.sa_model, 'pk', None)


class SAItemAddMixin(SAModelMixin, ahth.ItemMixin, metaclass=ABCMeta):
    def sa_add(self, *, key: Optional[str] = None) -> None:
        self.sa_session(key).add(self.item)


class SAItemDeleteMixin(
    SAModelDeleteMixin,
    SAPrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_sa_delete_stmt(self, model: Any = None) -> Delete:
        return super(). \
            get_sa_delete_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class SAItemEditMixin(
    ahth.ItemMixin,
    SAModelEditMixin,
    SAPrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_sa_edit_stmt(self, model: Any = None) -> Update:
        return super(). \
            get_sa_update_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class SAItemViewMixin(
    ahth.ItemMixin,
    SAModelViewMixin,
    SAPrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_sa_view_stmt(self, model: Any = None) -> Select:
        return super(). \
            get_sa_select_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class SAListAddMixin(ahth.ListMixin, SAModelMixin, metaclass=ABCMeta):
    items: List[Any]

    def sa_add_all(self, *, key: Optional[str] = None) -> None:
        self.sa_session(key).add_all(self.items)


class SAListDeleteMixin(ahth.ListMixin, SAModelDeleteMixin, metaclass=ABCMeta):
    pass


class SAListEditMixin(ahth.ListMixin, SAModelEditMixin, metaclass=ABCMeta):
    pass


class SAListViewMixin(
    ahth.ListMixin,
    ahth.PaginationMixin,
    SAModelViewMixin,
    metaclass=ABCMeta,
):
    pass


class SABaseView(View, SAMixin):
    """SQLAlchemy class based view."""


class SAModelView(View, SAModelMixin):
    """SQLAlchemy single model class based view."""


SAView = SAModelView
