from abc import ABCMeta
from typing import Any, List, Optional

import aiohttp_things as ahth
from aiohttp.web import View
from aiohttp.web_urldispatcher import AbstractRoute
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Select, Update
from sqlalchemy_things.pagination import OffsetPage, OffsetPaginator

from aiohttp_sqlalchemy.constants import SA_DEFAULT_KEY
from aiohttp_sqlalchemy.deprecation import _handle_deprecation
from aiohttp_sqlalchemy.utils import get_session


class SAMixin(ahth.ContextMixin, metaclass=ABCMeta):
    sa_session_key: str = SA_DEFAULT_KEY

    def get_sa_session(self, key: Optional[str] = None) -> AsyncSession:
        return get_session(self.request, key or self.sa_session_key)


class SAModelMixin(SAMixin, metaclass=ABCMeta):
    sa_model: Any = None  # Not all developers use declarative mapping


class DeleteStatementMixin(SAModelMixin):
    def get_delete_stmt(self, model: Any = None) -> Delete:
        return delete(model or self.sa_model)


class UpdateStatementMixin(SAModelMixin):
    def get_update_stmt(self, model: Any = None) -> Update:
        return update(model or self.sa_model)


class SelectStatementMixin(SAModelMixin):
    def get_select_stmt(self, model: Any = None) -> Select:
        return select(model or self.sa_model)


class OffsetPaginationMixin(ahth.PaginationMixin, SelectStatementMixin):
    page_key: int = 1
    page_key_adapter = int
    paginator: OffsetPaginator = OffsetPaginator()

    async def execute_select_stmt(
        self,
        model: Any = None,
        key: Optional[str] = None,
    ) -> Optional[OffsetPage]:
        async with self.get_sa_session().begin():
            page = await self.paginator.get_page_async(
                self.get_sa_session(key or self.sa_session_key),
                self.get_select_stmt(model or self.sa_model),
                self.page_key,
            )
        return page

    async def prepare_context(self) -> None:
        page: Optional[OffsetPage] = await self.execute_select_stmt()

        if page:
            route: AbstractRoute = self.request.match_info.route

            self.context['items'] = page.items

            if page.next:
                next_ = str(page.next)
                self.context['next_url'] = route.url_for(page_key=next_)
            else:
                self.context['next_url'] = page.next

            if page.previous:
                previous_ = str(page.previous)
                self.context['previous_url'] = route.url_for(page_key=previous_)
            else:
                self.context['previous_url'] = page.previous


class PrimaryKeyMixin(ahth.PrimaryKeyMixin, SAModelMixin, metaclass=ABCMeta):
    sa_pk_attr: Any = getattr(SAModelMixin.sa_model, 'pk', None)


class ItemAddMixin(SAModelMixin, ahth.ItemMixin, metaclass=ABCMeta):
    def sa_add(self, *, key: Optional[str] = None) -> None:
        self.get_sa_session(key).add(self.item)


class ItemDeleteMixin(
    DeleteStatementMixin,
    PrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_delete_stmt(self, model: Any = None) -> Delete:
        return super(). \
            get_delete_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class ItemEditMixin(
    ahth.ItemMixin,
    UpdateStatementMixin,
    PrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_update_stmt(self, model: Any = None) -> Update:
        return super(). \
            get_update_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class ItemViewMixin(
    ahth.ItemMixin,
    SelectStatementMixin,
    PrimaryKeyMixin,
    metaclass=ABCMeta,
):
    def get_select_stmt(self, model: Any = None) -> Select:
        return super(). \
            get_select_stmt(model). \
            where(self.sa_pk_attr == self.pk)


class ListAddMixin(ahth.ListMixin, SAModelMixin, metaclass=ABCMeta):
    items: List[Any]

    def sa_add_all(self, *, key: Optional[str] = None) -> None:
        self.get_sa_session(key).add_all(self.items)


class ListDeleteMixin(ahth.ListMixin, DeleteStatementMixin, metaclass=ABCMeta):
    pass


class ListEditMixin(ahth.ListMixin, UpdateStatementMixin, metaclass=ABCMeta):
    pass


class ListViewMixin(
    ahth.ListMixin,
    SelectStatementMixin,
    metaclass=ABCMeta,
):
    pass


class SABaseView(View, SAMixin):
    pass


class SAModelView(View, SAModelMixin):
    pass


def __getattr__(name: str) -> Any:
    name = _handle_deprecation(name)
    if name:
        return globals().get(name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
