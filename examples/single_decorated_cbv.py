from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_decorator, sa_bind, SAView
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


metadata = sa.MetaData()
Base: 'Any' = orm.declarative_base(metadata=metadata)


class Request(Base):
    __tablename__ = 'requests'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


class Main(SAView):
    @sa_decorator()
    async def get(self):
        async with self.request['sa_main'].bind.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with self.sa_session().begin():
            self.sa_session().add_all([Request()])
            result = await self.sa_session().execute(sa.select(Request))
            data = {r.id: r.timestamp.isoformat() for r in result.scalars()}
            return web.json_response(data)


app = web.Application()

engine = create_async_engine('sqlite+aiosqlite:///')
Session = orm.sessionmaker(engine, AsyncSession)
aiohttp_sqlalchemy.setup(app, [sa_bind(Session, middleware=False)])

app.add_routes([web.view('/', Main)])

if __name__ == '__main__':
    web.run_app(app)
