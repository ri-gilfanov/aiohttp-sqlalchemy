==================
aiohttp-sqlalchemy
==================
|Release| |Python versions| |Downloads count| |Build status| |Test coverage| |Documantation|

.. |Release| image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Release

.. |Python versions| image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Python versions

.. |Downloads count| image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy
  :target: https://pypistats.org/packages/aiohttp-sqlalchemy
  :alt: Downloads count

.. |Build status| image:: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy.svg?branch=master
  :target: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy
  :alt: Build status

.. |Test coverage| image:: https://coveralls.io/repos/github/ri-gilfanov/aiohttp-sqlalchemy/badge.svg?branch=master
  :target: https://coveralls.io/github/ri-gilfanov/aiohttp-sqlalchemy?branch=master
  :alt: Test coverage

.. |Documantation| image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation

SQLAlchemy 1.4 / 2.0 support for aiohttp.

The library provides the next features:

* initializing asynchronous sessions through a middlewares;
* initializing asynchronous sessions through a decorators;
* simple access to one asynchronous session by default key;
* preventing attributes from being expired after commit by default;
* support for different types of request handlers.


Documentation
-------------
https://aiohttp-sqlalchemy.readthedocs.io


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
  from aiohttp_sqlalchemy import sa_session
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
          items = result.scalars()

      data = {}
      for item in items:
          data[item.pk] = item.timestamp.isoformat()

      return web.json_response(data)


  async def app_factory():
      app = web.Application()

      aiohttp_sqlalchemy.setup(app, [
          aiohttp_sqlalchemy.bind('sqlite+aiosqlite:///'),
      ])
      await aiohttp_sqlalchemy.init_db(app, metadata)

      app.add_routes([web.get('/', main)])

      return app

  if __name__ == '__main__':
      web.run_app(app_factory())

