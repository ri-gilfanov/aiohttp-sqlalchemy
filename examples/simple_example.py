from datetime import datetime

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy import orm

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_session

metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class MyModel(Base):
    __tablename__ = "my_table"

    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    db_session = sa_session(request)

    async with db_session.begin():
        db_session.add(MyModel())
        result = await db_session.execute(sa.select(MyModel))
        result = result.scalars()

    data = {instance.pk: instance.timestamp.isoformat() for instance in result}
    return web.json_response(data)


async def app_factory():
    app = web.Application()

    bind = aiohttp_sqlalchemy.bind("sqlite+aiosqlite:///")
    aiohttp_sqlalchemy.setup(app, [bind])
    await aiohttp_sqlalchemy.init_db(app, metadata)

    app.add_routes([web.get("/", main)])

    return app


if __name__ == "__main__":
    web.run_app(app_factory())
