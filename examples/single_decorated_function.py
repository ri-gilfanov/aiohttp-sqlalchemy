from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_decorator, sa_engine
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import create_async_engine


metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


@sa_decorator()
async def main(request):
    async with request.app['sa_main'].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with request['sa_main'].begin():
        request['sa_main'].add_all([Request()])
        result = await request['sa_main'].execute(sa.select(Request))
        data = {r.id: r.timestamp.isoformat() for r in result.scalars()}
        return web.json_response(data)


app = web.Application()
engine = create_async_engine('sqlite+aiosqlite:///')
aiohttp_sqlalchemy.setup(app, [sa_engine(engine, middleware=False)])
app.add_routes([web.get('/', main)])
web.run_app(app)
