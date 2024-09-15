from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
import sqlalchemy as sa
from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request
from sqlalchemy import orm
from sqlalchemy_things.pagination import OffsetPage

if TYPE_CHECKING:  # pragma: no cover
    from aiohttp.web import Request
    from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    ListAddMixin,
    OffsetPaginationMixin,
    SABaseView,
    UnitAddMixin,
    UnitDeleteMixin,
    UnitEditMixin,
    UnitViewMixin,
    init_db,
)


def test_sa_session(
    mocked_request: Request,
    session: AsyncSession,
) -> None:
    mocked_request[SA_DEFAULT_KEY] = session
    view = SABaseView(mocked_request)
    assert view.get_sa_session() is session
    with pytest.raises(TypeError):
        view.get_sa_session("wrong key")


def test_instance_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper[Any],
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class ItemAdd(web.View, UnitAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ItemAdd(mocked_request)
    view.item = Model()
    view.sa_add()


def test_delete_stmt(mocked_request: Request, base_model: orm.Mapper[Any]) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class ItemDelete(web.View, UnitDeleteMixin):
        sa_model = Model

    view = ItemDelete(mocked_request)
    view.get_delete_stmt()


def test_edit_stmt(mocked_request: Request, base_model: orm.Mapper[Any]) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceEdit(web.View, UnitEditMixin):
        sa_model = Model

    view = InstanceEdit(mocked_request)
    view.get_update_stmt()


def test_view_stmt(mocked_request: Request, base_model: orm.Mapper[Any]) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceView(web.View, UnitViewMixin):
        sa_model = Model

    view = InstanceView(mocked_request)
    view.get_select_stmt()


async def test_offset_pagination(
    middlewared_app: web.Application,
    session: AsyncSession,
    base_model: orm.Mapper[Any],
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class OffsetPaginationHandler(web.View, OffsetPaginationMixin):
        sa_model = Model

    await init_db(middlewared_app, Model.metadata)

    request = make_mocked_request(METH_GET, "/?page_key=1")
    request[SA_DEFAULT_KEY] = session
    handler = OffsetPaginationHandler(request)
    assert handler.page_key == 1
    page = await handler.execute_select_stmt()
    isinstance(page, OffsetPage)
    await handler.prepare_context()
    assert list(handler.context["items"]) == []
    assert handler.context["previous_url"] is None
    assert handler.context["next_url"] is None

    page_size = handler.paginator.page_size

    async with session.begin():
        session.add_all([Model() for i in range(page_size + 1)])

    page = await handler.execute_select_stmt()
    isinstance(page, OffsetPage)
    await handler.prepare_context()
    assert len(list(handler.context["items"])) == page_size
    assert handler.context["previous_url"] is None
    assert handler.context["next_url"] is not None

    request = make_mocked_request(METH_GET, "/?page_key=2")
    request[SA_DEFAULT_KEY] = session
    handler = OffsetPaginationHandler(request)
    assert handler.page_key == 2
    page = await handler.execute_select_stmt()
    isinstance(page, OffsetPage)
    await handler.prepare_context()
    assert len(list(handler.context["items"])) == 1
    assert handler.context["previous_url"] is not None
    assert handler.context["next_url"] is None


def test_list_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper[Any],
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = "model"

        pk = sa.Column(sa.Integer, primary_key=True)

    class ListAdd(web.View, ListAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ListAdd(mocked_request)
    view.items.append(Model())
    view.items.append(Model())
    view.sa_add_all()
