==========
Quickstart
==========

Simple example
--------------
Install ``aiosqlite`` for work with sqlite3: ::

  pip install aiosqlite

Copy and paste this code in a file and run:

.. code-block:: python

  from datetime import datetime

  import sqlalchemy as sa
  from aiohttp import web
  from sqlalchemy import orm

  import aiohttp_sqlalchemy
  from aiohttp_sqlalchemy import sa_session

  metadata = sa.MetaData()
  Base = orm.declarative_base(metadata=metadata)


  class MyModel(Base):
      __tablename__ = "my_table"

      pk = sa.Column(sa.Integer, primary_key=True)
      timestamp = sa.Column(sa.DateTime(), default=datetime.now)


  async def main(request):
      db_session = sa_session(request)

      async with db_session.begin():
          db_session.add(MyModel())
          result = await db_session.execute(sa.select(MyModel))
          result = result.scalars()

      data = {
          instance.pk: instance.timestamp.isoformat()
          for instance in result
      }
      return web.json_response(data)


  async def app_factory():
      app = web.Application()

      bind = aiohttp_sqlalchemy.bind("sqlite+aiosqlite:///")
      aiohttp_sqlalchemy.setup(app, [bind])
      await aiohttp_sqlalchemy.init_db(app, metadata)

      app.add_routes([web.get("/", main)])

      return app


  if __name__ == "__main__":
      web.run_app(app_factory())


SQLAlchemy and Asyncio
----------------------
See `Asynchronous I/O (asyncio) <https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html>`_
section in SQLAlchemy 1.4 documentation.


More control in configuration
-----------------------------
.. code-block:: python

  import aiohttp_sqlalchemy
  from sqlalchemy import orm

  url = 'sqlite+aiosqlite:///'
  engine = create_async_engine(url, echo=True)
  Session = orm.sessionmaker(main_engine, AsyncSession, expire_on_commit=False)

  aiohttp_sqlalchemy.setup(app, [
      aiohttp_sqlalchemy.bind(Session),
  ])


Class based views
-----------------
.. code-block:: python

  from aiohttp import web
  from aiohttp_sqlalchemy import SAView


  class MyClassBasedView(SAView):
      async def get(self):
          db_session = self.sa_session()

          async with db_session.begin():
              # some your code


  aiohttp_sqlalchemy.setup(app, [
      aiohttp_sqlalchemy.bind(MainSession),
  ])
  app.add_routes([web.view("/", MyClassBasedView)])
