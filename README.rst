==================
aiohttp-sqlalchemy
==================
.. image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg
  :target: https://badge.fury.io/py/aiohttp-sqlalchemy

.. image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy
  :target: https://pypistats.org/packages/aiohttp-sqlalchemy
  :alt: Downloads count

.. image:: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy.svg?branch=master
  :target: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy

.. image:: https://coveralls.io/repos/github/ri-gilfanov/aiohttp-sqlalchemy/badge.svg?branch=master
  :target: https://coveralls.io/github/ri-gilfanov/aiohttp-sqlalchemy?branch=master

SQLAlchemy 1.4 / 2.0 support for aiohttp.

Library forward a ``sqlalchemy.ext.asyncio.AsyncSession`` object as
``request['sa_main']`` or ``SAView.sa_session()`` by default.


Documentation
-------------
https://aiohttp-sqlalchemy.readthedocs.io/


Installation
------------
::

    pip install aiohttp-sqlalchemy


Simple example
--------------
Install ``aiosqlite`` for work with sqlite3: ::

  pip install aiosqlite

Copy and paste this code in a file and run:

.. code-block:: python

  from aiohttp import web
  import aiohttp_sqlalchemy
  from aiohttp_sqlalchemy import sa_bind
  from datetime import datetime
  import sqlalchemy as sa
  from sqlalchemy import orm
  from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


  metadata = sa.MetaData()
  Base = orm.declarative_base(metadata=metadata)


  class MyModel(Base):
      __tablename__ = 'my_table'
      id = sa.Column(sa.Integer, primary_key=True)
      timestamp = sa.Column(sa.DateTime(), default=datetime.now)


  async def main(request):
      async with request['sa_main'].bind.begin() as conn:
          await conn.run_sync(Base.metadata.create_all)

      async with request['sa_main'].begin():
          request['sa_main'].add_all([MyModel()])
          result = await request['sa_main'].execute(sa.select(MyModel))
          data = {r.id: r.timestamp.isoformat() for r in result.scalars()}
          return web.json_response(data)


  app = web.Application()

  engine = create_async_engine('sqlite+aiosqlite:///')
  Session = orm.sessionmaker(engine, AsyncSession)
  aiohttp_sqlalchemy.setup(app, [sa_bind(Session)])

  app.add_routes([web.get('/', main)])

  if __name__ == '__main__':
      web.run_app(app)
