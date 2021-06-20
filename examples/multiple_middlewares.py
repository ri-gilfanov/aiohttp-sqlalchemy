from aiohttp import web
from datetime import datetime
from random import choice
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import TYPE_CHECKING

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind

if TYPE_CHECKING:
    from typing import Any


metadata = sa.MetaData()
Base: 'Any' = orm.declarative_base(metadata=metadata)


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    async with request['sa_main'].bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with request['sa_second'].bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = choice(['sa_main', 'sa_second'])

    async with request[session].begin():
        request[session].add_all([Request()])

    async with request['sa_main'].begin():
        result = await request['sa_main'].execute(sa.select(Request))
        main_result = {
            r.id: r.timestamp.isoformat()
            for r in result.scalars()
        }

    async with request['sa_second'].begin():
        result = await request['sa_second'].execute(sa.select(Request))
        secondary_result = {
            r.id: r.timestamp.isoformat()
            for r in result.scalars()
        }

    data = {
        'main': main_result,
        'secondary': secondary_result,
    }
    return web.json_response(data)


app = web.Application()

main_engine = create_async_engine('sqlite+aiosqlite:///')
second_engine = create_async_engine('sqlite+aiosqlite:///')

MainSession = orm.sessionmaker(main_engine, AsyncSession)
SecondSession = orm.sessionmaker(second_engine, AsyncSession)

aiohttp_sqlalchemy.setup(app, [
    sa_bind(MainSession),
    sa_bind(SecondSession, 'sa_second'),
])

app.add_routes([web.get('/', main)])

if __name__ == '__main__':
    web.run_app(app)
