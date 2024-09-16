from datetime import datetime

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy import orm

import aiohttp_sqlalchemy


class Base(orm.DeclarativeBase): ...


class MyModel(Base):
    __tablename__ = "my_table"

    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    sa_session = aiohttp_sqlalchemy.get_session(request)

    async with sa_session.begin():
        sa_session.add(MyModel())
        result = await sa_session.execute(sa.select(MyModel))
        result = result.scalars()

    data = {instance.pk: instance.timestamp.isoformat() for instance in result}
    return web.json_response(data)


async def app_factory():
    app = web.Application()

    aiohttp_sqlalchemy.setup(
        app,
        [
            aiohttp_sqlalchemy.bind("sqlite+aiosqlite:///"),
        ],
    )
    await aiohttp_sqlalchemy.init_db(app, Base.metadata)

    app.add_routes([web.get("/", main)])
    return app


if __name__ == "__main__":
    web.run_app(app_factory(), port=8087)
