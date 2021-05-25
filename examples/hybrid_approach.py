from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_decorator, sa_bind
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine
from random import choice


metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


@sa_decorator('sa_secondary')
async def main(request):
    async with request.app['sa_main'].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with request.app['sa_secondary'].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = choice(['sa_main', 'sa_secondary'])

    async with request[session].begin():
        request[session].add_all([Request()])

    async with request['sa_main'].begin():
        result = await request['sa_main'].execute(sa.select(Request))
        main_result = {r.id: r.timestamp.isoformat() for r in result.scalars()}

    async with request['sa_secondary'].begin():
        result = await request['sa_secondary'].execute(sa.select(Request))
        secondary_result = {r.id: r.timestamp.isoformat() for r in result.scalars()}

    data = {
        'main': main_result,
        'secondary': secondary_result,
    }
    return web.json_response(data)


app = web.Application()

main_engine = create_async_engine('sqlite+aiosqlite:///')
secondary_engine = create_async_engine('sqlite+aiosqlite:///')

aiohttp_sqlalchemy.setup(app, [
    sa_bind(main_engine),
    sa_bind(secondary_engine, 'sa_secondary', middleware=False),
])

app.add_routes([web.get('/', main)])
web.run_app(app)
