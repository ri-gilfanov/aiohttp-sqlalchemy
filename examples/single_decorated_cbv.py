import sqlalchemy as sa
from aiohttp import web

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import SAView, sa_decorator
from examples.base import DB_URL, MyModel, metadata


class Main(SAView):
    @sa_decorator()
    async def get(self):
        async with self.sa_session().begin():
            self.sa_session().add_all([MyModel()])
            stmt = sa.select(MyModel)
            result = await self.sa_session().execute(stmt)
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

    app.add_routes([web.view("/", Main)])

    return app


if __name__ == "__main__":
    web.run_app(app_factory())
