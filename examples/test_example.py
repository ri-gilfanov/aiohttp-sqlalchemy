from datetime import datetime
from secrets import choice
from typing import Any

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy import orm

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import (
    SA_DEFAULT_KEY,
    SAMixin,
    sa_decorator,
    sa_session,
)

metadata = sa.MetaData()
Base: Any = orm.declarative_base(metadata=metadata)
DB_URL = "sqlite+aiosqlite:///"


class MyModel(Base):
    __tablename__ = "my_table"
    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


FIRST_KEY = SA_DEFAULT_KEY
SECOND_KEY = "sa_second"
THIRD_KEY = "sa_third"
FOURTH_KEY = "sa_fourth"

KEY_LIST = [FIRST_KEY, SECOND_KEY, THIRD_KEY, FOURTH_KEY]


async def add_instance(session):
    async with session.begin():
        session.add_all([MyModel()])


async def select_instances(session):
    async with session.begin():
        stmt = sa.select(MyModel)
        result = await session.execute(stmt)
        instances = result.scalars()
        return {instance.pk: instance.timestamp.isoformat() for instance in instances}


@sa_decorator(THIRD_KEY)
@sa_decorator(FOURTH_KEY)
async def function_handler(request):
    await add_instance(sa_session(request, choice(KEY_LIST)))
    return web.json_response(
        {key: await select_instances(sa_session(request, key)) for key in KEY_LIST}
    )


class ClassOrganizedHandler:
    @sa_decorator(THIRD_KEY)
    @sa_decorator(FOURTH_KEY)
    async def get(self, request):
        await add_instance(sa_session(request, choice(KEY_LIST)))
        return web.json_response(
            {key: await select_instances(sa_session(request, key)) for key in KEY_LIST}
        )


class ClassBasedView(web.View, SAMixin):
    @sa_decorator(THIRD_KEY)
    @sa_decorator(FOURTH_KEY)
    async def get(self):
        await add_instance(self.get_sa_session(choice(KEY_LIST)))
        return web.json_response(
            {key: await select_instances(self.get_sa_session(key)) for key in KEY_LIST}
        )


async def app_factory():
    app = web.Application()
    aiohttp_sqlalchemy.setup(
        app,
        [
            aiohttp_sqlalchemy.bind(DB_URL),
            aiohttp_sqlalchemy.bind(DB_URL, SECOND_KEY),
            aiohttp_sqlalchemy.bind(DB_URL, THIRD_KEY, middleware=False),
            aiohttp_sqlalchemy.bind(DB_URL, FOURTH_KEY, middleware=False),
        ],
    )
    for key in KEY_LIST:
        await aiohttp_sqlalchemy.init_db(app, metadata, key)

    app.add_routes([web.get("/handler_a", function_handler)])
    app.add_routes([web.get("/handler_b", ClassOrganizedHandler().get)])
    app.add_routes([web.view("/handler_c", ClassBasedView)])

    return app


if __name__ == "__main__":
    web.run_app(app_factory(), port=8087)
