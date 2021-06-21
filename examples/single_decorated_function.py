import sqlalchemy as sa
from aiohttp import web

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_decorator, sa_session
from examples.base import DB_URL, MyModel, metadata


@sa_decorator()
async def main(request):
    db_session = sa_session(request)

    async with db_session.begin():
        db_session.add_all([MyModel()])
        stmt = sa.select(MyModel)
        result = await db_session.execute(stmt)
        instances = result.scalars()

    data = {}
    for instance in instances:
        data[instance.pk] = instance.timestamp.isoformat()

    return web.json_response(data)


async def app_factory():
    app = web.Application()

    bind = aiohttp_sqlalchemy.bind(DB_URL, middleware=False)
    aiohttp_sqlalchemy.setup(app, [bind])
    await aiohttp_sqlalchemy.init_db(app, metadata)

    app.add_routes([web.get("/", main)])

    return app


if __name__ == "__main__":
    web.run_app(app_factory())
