import pytest
import sqlalchemy as sa
from aiohttp import web
from aiohttp.web import Request
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession

from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    SABaseView,
    SAInstanceDeleteMixin,
    SAInstanceGetMixin,
    SAInstancePostMixin,
    SAInstancePutMixin,
    SAListPostMixin,
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


def test_instance_get(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceView(web.View, SAInstanceGetMixin):
        sa_model = Model

    view = InstanceView(mocked_request)
    view.get_sa_view_stmt()


def test_instance_delete(
    mocked_request: Request,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceDelete(web.View, SAInstanceDeleteMixin):
        sa_model = Model

    view = InstanceDelete(mocked_request)
    view.get_sa_delete_stmt()


def test_instance_post(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceAdd(web.View, SAInstancePostMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = InstanceAdd(mocked_request)
    view.instance = Model()
    view.sa_add()


def test_instance_put(mocked_request: Request, base_model: orm.Mapper) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class InstanceEdit(web.View, SAInstancePutMixin):
        sa_model = Model

    view = InstanceEdit(mocked_request)
    view.get_sa_edit_stmt()


def test_list_post(
    mocked_request: Request,
    session: AsyncSession,
    base_model: orm.Mapper,
) -> None:
    class Model(base_model):  # type: ignore
        __tablename__ = 'model'

        pk = sa.Column(sa.Integer, primary_key=True)

    class ListAdd(web.View, SAListPostMixin):
        sa_model = Model

    mocked_request[SA_DEFAULT_KEY] = session
    view = ListAdd(mocked_request)
    view.items.append(Model())
    view.items.append(Model())
    view.sa_add_all()
