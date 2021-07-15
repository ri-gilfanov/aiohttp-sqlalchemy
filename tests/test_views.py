import pytest
import sqlalchemy as sa
from aiohttp import web
from aiohttp.web import Request
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    SABaseView,
    SAItemAddMixin,
    SAItemDeleteMixin,
    SAItemEditMixin,
    SAItemViewMixin,
    SAListAddMixin,
)


def test_sa_session(
    mocked_request: Request,
    session: AsyncSession,
) -> None:
    mocked_request[SA_DEFAULT_KEY] = session
    view = SABaseView(mocked_request)
    assert view.sa_session() is session
    with pytest.raises(TypeError):
        view.sa_session('wrong key')


def test_instance_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceAdd(web.View, SAItemAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = InstanceAdd(mocked_request)
    view.item = Model()
    view.sa_add()


def test_delete_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceDelete(web.View, SAItemDeleteMixin):
        sa_model = Model

    view = InstanceDelete(mocked_request)
    view.get_sa_delete_stmt()


def test_edit_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceEdit(web.View, SAItemEditMixin):
        sa_model = Model

    view = InstanceEdit(mocked_request)
    view.get_sa_edit_stmt()


def test_view_stmt(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceView(web.View, SAItemViewMixin):
        sa_model = Model

    view = InstanceView(mocked_request)
    view.get_sa_view_stmt()


def test_list_add(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class ListAdd(web.View, SAListAddMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ListAdd(mocked_request)
    view.items.append(Model())
    view.items.append(Model())
    view.sa_add_all()
