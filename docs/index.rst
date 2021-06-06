.. aiohttp-sqlalchemy documentation master file, created by
  sphinx-quickstart on Tue Apr  6 16:59:03 2021.
  You can adapt this file completely to your liking, but it should at least
  contain the root `toctree` directive.

==============================================
Welcome to aiohttp-sqlalchemy's documentation!
==============================================
.. toctree::
  :maxdepth: 2
  :caption: Contents:

.. contents:: Table of Contents
  :depth: 2
  :local:


Overview
--------
SQLAlchemy 1.4 / 2.0 support for aiohttp.

Library forward a ``sqlalchemy.ext.asyncio.AsyncSession`` object as
``request['sa_main']`` or ``SAView.sa_session()`` by default.


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
  from aiohttp_sqlalchemy import sa_bind, sa_middleware
  from datetime import datetime
  import sqlalchemy as sa
  from sqlalchemy import orm
  from sqlalchemy.ext.asyncio import create_async_engine


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
  aiohttp_sqlalchemy.setup(app, [sa_bind(engine)])

  app.add_routes([web.get('/', main)])
  web.run_app(app)


SQLAlchemy and Asyncio
----------------------
See `Asynchronous I/O (asyncio) <https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html>`_
section in SQLAlchemy 1.4 Documentation.


Binding multiple engines
------------------------
.. code-block:: python

  main_engine = create_async_engine('postgresql+asyncpg://user:password@host/database')
  second_engine = create_async_engine('mysql+aiomysql://user:password@host/database')
  third_engine = create_async_engine('sqlite+aiosqlite:///')

  aiohttp_sqlalchemy.setup(app, [
      sa_bind(main_engine),
      sa_bind(second_engine, 'sa_second'),
      sa_bind(third_engine, 'sa_third'),
  ])


Class based views
-----------------
.. code-block:: python

  from aiohttp_sqlalchemy import SAView

  class Handler(SAView):
      async def get(self):
          async with self.sa_session().begin():
              # some your code

          async with self.sa_session('sa_second').begin():
              # some your code

  main_engine = create_async_engine('sqlite+aiosqlite:///')
  second_engine = create_async_engine('sqlite+aiosqlite:///')
  aiohttp_sqlalchemy.setup(app, [
    sa_bind(main_engine),
    sa_bind(second_engine, 'sa_second'),
  ])


Decorating handlers
-------------------
.. warning::

  For use a some ``AsyncEngine`` in decorators, you must set a ``middleware``
  argument to ``False`` in ``sa_bind`` call. Else will raise an exception
  ``DuplicateRequestKeyError``.

.. code-block:: python

  @sa_decorator('sa_fourth')
  async def handler(request):
      # some your code

  class Handler(SAView):
      @sa_decorator('sa_fourth')
      async def get(self):
          # some your code

  engine = create_async_engine('sqlite+aiosqlite:///')
  aiohttp_sqlalchemy.setup(app, [
      sa_bind(engine, 'sa_fourth', middleware=False),
  ])


Nested apps
-----------
.. code-block:: python

  async def main(request):
      async with request['sa_main'].bind.begin() as conn:
          # some operations with AsyncConnection object with
          # an AsyncTransaction established.

      async with request['sa_main'].begin():
          # some operations with AsyncSession object

  app = web.Application()

  engine = create_async_engine('sqlite+aiosqlite:///')
  aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])

  subapp = web.Application()
  subapp.add_routes([web.get('', main)])

  app.add_subapp(prefix='/subapp', subapp=subapp)


Change log
----------
Version 0.7.0
^^^^^^^^^^^^^
Removed
"""""""
Removed support of ``request.config_dict.get('sa_main')`` and
``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind``
expression.

Version 0.6.0
^^^^^^^^^^^^^
Added
"""""
Add support ``sqlalchemy.orm.sessionmaker`` as a first argument in function
``sa_bind(arg, key, middleware)``.

Changed
"""""""
Argument ``engine: AsyncEngine`` changed to ``arg: Union[AsyncEngine,
sessionmaker]`` in ``sa_bind()`` signature.

Deprecated
""""""""""
Deprecated support of ``request.config_dict.get('sa_main')`` and
``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind``
expression.

Removed
"""""""
Deprecated class ``views.SAViewMixin`` is removed. Use
``views.SAAbstractView``.

Deprecated attribute ``SAView.sa_main_session`` is removed. Use method
``SAView.sa_session(key: str = 'sa_main')``.

Version 0.5.0
^^^^^^^^^^^^^
Removed
"""""""
Deprecated function ``aiohttp_sqlalchemy.sa_engine()`` is removed. Use
``aiohttp_sqlalchemy.sa_bind()``.

Deprecated
""""""""""
Undocumented class ``views.SAViewMixin`` is deprecated. Use
``views.SAAbstractView``.

Version 0.4.0
^^^^^^^^^^^^^
Added
"""""
``SAView.sa_session(key: str = 'sa_main')`` function is added instead
``SAView.sa_main_session``.

Deprecated
""""""""""
``SAView.sa_main_session`` is deprecated. Use
``SAView.sa_session(key: str = 'sa_main')``.

Version 0.3.0
^^^^^^^^^^^^^
Added
"""""
``aiohttp_sqlalchemy.sa_bind()`` function is added instead
``aiohttp_sqlalchemy.sa_engine()``.

Deprecated
""""""""""
``aiohttp_sqlalchemy.sa_engine()`` function is deprecated. Use
``aiohttp_sqlalchemy.sa_bind()``.
