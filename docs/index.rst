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
.. image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue
  :target: https://pypi.org/project/aiohttp-sqlalchemy/

.. image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy
  :target: https://pypistats.org/packages/aiohttp-sqlalchemy
  :alt: Downloads count

.. image:: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy.svg?branch=master
  :target: https://travis-ci.com/ri-gilfanov/aiohttp-sqlalchemy

.. image:: https://coveralls.io/repos/github/ri-gilfanov/aiohttp-sqlalchemy/badge.svg?branch=master
  :target: https://coveralls.io/github/ri-gilfanov/aiohttp-sqlalchemy?branch=master

SQLAlchemy 1.4 / 2.0 support for aiohttp.

The library provides the next features:

* initializing asynchronous sessions through a middlewares;
* initializing asynchronous sessions through a decorators;
* simple access to one asynchronous session by default key;
* support for different types of request handlers.


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
  from aiohttp_sqlalchemy import sa_bind, sa_session
  from datetime import datetime
  import sqlalchemy as sa
  from sqlalchemy import orm


  metadata = sa.MetaData()
  Base = orm.declarative_base(metadata=metadata)


  class MyModel(Base):
      __tablename__ = 'my_table'
      id = sa.Column(sa.Integer, primary_key=True)
      timestamp = sa.Column(sa.DateTime(), default=datetime.now)


  async def main(request):
      db_session = sa_session(request)

      async with db_session.bind.begin() as connection:
          await connection.run_sync(Base.metadata.create_all)

      async with db_session.begin():
          db_session.add_all([MyModel()])
          result = await db_session.execute(sa.select(MyModel))
          data = {record.id: record.timestamp.isoformat()
                  for record in result.scalars()}
          return web.json_response(data)


  app = web.Application()

  aiohttp_sqlalchemy.setup(app, [sa_bind('sqlite+aiosqlite:///')])

  app.add_routes([web.get('/', main)])

  if __name__ == '__main__':
      web.run_app(app)


SQLAlchemy and Asyncio
----------------------
See `Asynchronous I/O (asyncio) <https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html>`_
section in SQLAlchemy 1.4 documentation.


Binding multiple session factories
----------------------------------
.. code-block:: python

  from aiohttp_sqlalchemy import sa_bind

  main_engine = create_async_engine('postgresql+asyncpg://user:password@host/database')
  second_engine = create_async_engine('mysql+aiomysql://user:password@host/database')
  third_engine = create_async_engine('sqlite+aiosqlite:///')

  MainSession = orm.sessionmaker(main_engine, AsyncSession, expire_on_commit=False)
  SecondSession = orm.sessionmaker(second_engine, AsyncSession, expire_on_commit=False)
  ThirdSession = orm.sessionmaker(third_engine, AsyncSession, expire_on_commit=False)

  aiohttp_sqlalchemy.setup(app, [
      sa_bind(MainSession),
      sa_bind(SecondSession, 'sa_second'),
      sa_bind(ThirdSession, 'sa_third'),
  ])

Binding multiple engines to one session factory
-----------------------------------------------
See `Partitioning Strategies (e.g. multiple database backends per Session)
<https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session>`_
section in SQLAlchemy 1.4 documentation.

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

  aiohttp_sqlalchemy.setup(app, [
    sa_bind(MainSession),
    sa_bind(SecondSession, 'sa_second'),
  ])


Decorating handlers
-------------------
.. warning::

  For use a some ``AsyncEngine`` in decorators, you must set a ``middleware``
  argument to ``False`` in ``sa_bind`` call. Else will raise an exception
  ``DuplicateRequestKeyError``.

.. code-block:: python

  @sa_decorator('sa_optional')
  async def handler(request):
      # some your code

  class Handler(SAView):
      @sa_decorator('sa_optional')
      async def get(self):
          # some your code

  aiohttp_sqlalchemy.setup(app, [
      sa_bind(Session, 'sa_optional', middleware=False),
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
  Session = orm.sessionmaker(engine, AsyncSession, expire_on_commit=False)
  aiohttp_sqlalchemy.setup(app, [sa_engine(Session)])

  subapp = web.Application()
  subapp.add_routes([web.get('', main)])

  app.add_subapp(prefix='/subapp', subapp=subapp)


Change log
----------
Version 0.13
^^^^^^^^^^^^
Changed
"""""
* Argument ``expire_on_commit`` of ``sessionmaker`` set to ``False``
  by default.

Version 0.12
^^^^^^^^^^^^
Added
"""""
* Added ``sa_session_key`` attribute in ``SAAbstractView`` class.
* Added support url and ``AssyncEngine`` instance as first argument
  in ``sa_bind()``.

Changed
"""""""
* Rename first argument from ``factory`` to ``bind_to`` in ``sa_bind()``.
  signature.

Version 0.11
^^^^^^^^^^^^
Added
"""""
* Added ``sa_session(request, key='sa_main')`` utility.

Version 0.10
^^^^^^^^^^^^
Added
"""""
* Added support Python 3.7.

Version 0.9
^^^^^^^^^^^
Added
"""""
* Support of `organized handlers in class
  <https://docs.aiohttp.org/en/stable/web_quickstart.html#organizing-handlers-in-classes>`_
  added to ``sa_decorator(key)``.

Removed
"""""""
* Removed support of ``AsyncEngine`` type in ``sa_bind()`` signature. Use
  ``sessionmaker(engine, AsyncSession)`` or custom session factory returning
  ``AsyncSession`` instance.

Version 0.8
^^^^^^^^^^^
Changed
"""""""
* Rename first argument from ``arg`` to ``factory`` in ``sa_bind()``
  signature.

Deprecated
""""""""""
* ``AsyncEngine`` type is deprecated in ``sa_bind()`` signature. Use
  ``sessionmaker(engine, AsyncSession)`` or custom session factory returning
  ``AsyncSession`` instance.

Version 0.7
^^^^^^^^^^^
Changed
"""""""
* Usage ``sqlalchemy.orm.sessionmaker`` instance is recomended as a first
  argument for ``aiohttp_sqlalchemy.sa_bind()`` signature. See examples
  in documetation.

Removed
"""""""
* Removed support of ``request.config_dict.get('sa_main')`` and
  ``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind``
  expression.

Version 0.6
^^^^^^^^^^^
Added
"""""
* Add support ``sqlalchemy.orm.sessionmaker`` as a first argument in function
  ``sa_bind(arg, key, middleware)``.

Changed
"""""""
* Argument ``engine: AsyncEngine`` changed to ``arg: Union[AsyncEngine,
  sessionmaker]`` in ``sa_bind()`` signature.

Deprecated
""""""""""
* Deprecated support of ``request.config_dict.get('sa_main')`` and
  ``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind``
  expression.

Removed
"""""""
* Deprecated class ``views.SAViewMixin`` is removed. Use
  ``views.SAAbstractView``.
* Deprecated attribute ``SAView.sa_main_session`` is removed. Use method
  ``SAView.sa_session(key: str = 'sa_main')``.

Version 0.5
^^^^^^^^^^^
Removed
"""""""
* Deprecated function ``aiohttp_sqlalchemy.sa_engine()`` is removed. Use
  ``aiohttp_sqlalchemy.sa_bind()``.

Deprecated
""""""""""
* Undocumented class ``views.SAViewMixin`` is deprecated. Use
  ``views.SAAbstractView``.

Version 0.4
^^^^^^^^^^^
Added
"""""
* ``SAView.sa_session(key: str = 'sa_main')`` function is added instead
  ``SAView.sa_main_session``.

Deprecated
""""""""""
* ``SAView.sa_main_session`` is deprecated. Use
  ``SAView.sa_session(key: str = 'sa_main')``.

Version 0.3
^^^^^^^^^^^
Added
"""""
* ``aiohttp_sqlalchemy.sa_bind()`` function is added instead
  ``aiohttp_sqlalchemy.sa_engine()``.

Deprecated
""""""""""
* ``aiohttp_sqlalchemy.sa_engine()`` function is deprecated. Use
  ``aiohttp_sqlalchemy.sa_bind()``.
