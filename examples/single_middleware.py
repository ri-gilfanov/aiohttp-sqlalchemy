from aiohttp import web
import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind, sa_init_db, sa_session
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm


metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)


class MyModel(Base):
    __tablename__ = 'my_table'

    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)


async def main(request):
    db_session = sa_session(request)

    async with db_session.begin():
        db_session.add_all([MyModel()])
        stmt = sa.select(MyModel)
        result = await db_session.execute(stmt)
        items = result.scalars().all()

    data = {}
    for item in items:
        data[item.pk] = item.timestamp.isoformat()

    return web.json_response(data)


async def app_factory():
    app = web.Application()

    sa_binding = sa_bind('sqlite+aiosqlite:///')
    aiohttp_sqlalchemy.setup(app, [sa_binding])
    await sa_init_db(app, metadata)

    app.add_routes([web.get('/', main)])

    return app

if __name__ == '__main__':
    web.run_app(app_factory())
