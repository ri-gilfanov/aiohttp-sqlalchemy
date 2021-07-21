import pytest
import sqlalchemy as sa
from aiohttp import web
from aiohttp.hdrs import METH_GET
from aiohttp.test_utils import make_mocked_request
from aiohttp.web import Request
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_things.pagination import OffsetPage

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    ItemAddMixin,
    ItemDeleteMixin,
    ItemEditMixin,
    ItemViewMixin,
    ListAddMixin,
    OffsetPaginationMixin,
    SABaseView,
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
        view.get_sa_session('wrong key')


def test_instance_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class ItemAdd(web.View, ItemAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ItemAdd(mocked_request)
    view.item = Model()
    view.sa_add()


def test_delete_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class ItemDelete(web.View, ItemDeleteMixin):
        sa_model = Model

    view = ItemDelete(mocked_request)
    view.get_delete_stmt()


def test_edit_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceEdit(web.View, ItemEditMixin):
        sa_model = Model

    view = InstanceEdit(mocked_request)
    view.get_update_stmt()


def test_view_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceView(web.View, ItemViewMixin):
        sa_model = Model

    view = InstanceView(mocked_request)
    view.get_select_stmt()


async def test_offset_pagination(
    middlewared_app: web.Application,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class OffsetPaginationHandler(web.View, OffsetPaginationMixin):
        sa_model = Model

    await init_db(middlewared_app, Model.metadata)

    request = make_mocked_request(METH_GET, '/?page_key=2')
    request[SA_DEFAULT_KEY] = session
    handler = OffsetPaginationHandler(request)
    page = await handler.execute_select_stmt()
    isinstance(page, OffsetPage)


def test_list_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class ListAdd(web.View, ListAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ListAdd(mocked_request)
    view.items.append(Model())
    view.items.append(Model())
    view.sa_add_all()
