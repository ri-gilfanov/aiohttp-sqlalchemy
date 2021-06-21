from random import choice

import sqlalchemy as sa
from aiohttp import web

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_session
from examples.base import DB_URL, MyModel, metadata


async def main(request):
    data = {}
    main_session = sa_session(request)
    second_session = sa_session(request, "sa_second")
    random_session = choice([main_session, second_session])

    async with random_session.begin():
        random_session.add_all([MyModel()])

    main_session = sa_session(request)
    async with main_session.begin():
        stmt = sa.select(MyModel)
        result = await main_session.execute(stmt)
        instances = result.scalars()

    data["main"] = {
        instance.pk: instance.timestamp.isoformat() for instance in instances
    }

    second_session = sa_session(request, "sa_second")
    async with second_session.begin():
        stmt = sa.select(MyModel)
        result = await second_session.execute(stmt)
        instances = result.scalars()

    data["second"] = {
        instance.pk: instance.timestamp.isoformat() for instance in instances
    }

    return web.json_response(data)


async def app_factory():
    app = web.Application()
    aiohttp_sqlalchemy.setup(
        app,
        [
            aiohttp_sqlalchemy.bind(DB_URL),
            aiohttp_sqlalchemy.bind(DB_URL, "sa_second"),
        ],
    )
    await aiohttp_sqlalchemy.init_db(app, metadata)
    await aiohttp_sqlalchemy.init_db(app, metadata, "sa_second")
    app.add_routes([web.get("/", main)])
    return app


if __name__ == "__main__":
    web.run_app(app_factory())
