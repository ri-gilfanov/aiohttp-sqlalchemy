from aiohttp import web
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from typing import TYPE_CHECKING

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind, sa_session

if TYPE_CHECKING:
    from typing import Any


metadata = sa.MetaData()
Base: 'Any' = orm.declarative_base(metadata=metadata)


class MyModel(Base):
    __tablename__ = 'my_table'
    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    db_session = sa_session(request)

    async with db_session.bind.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with db_session.begin():
        db_session.add_all([MyModel()])
        result = await db_session.execute(sa.select(MyModel))
        items = result.scalars().all()

    data = {}
    for item in items:
        data[item.pk] = item.timestamp.isoformat()

    return web.json_response(data)


app = web.Application()
binding = sa_bind('sqlite+aiosqlite:///')
aiohttp_sqlalchemy.setup(app, [binding])
app.add_routes([web.get('/', main)])

if __name__ == '__main__':
    web.run_app(app)
