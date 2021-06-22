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
  :depth: 1
  :local:


Overview
--------
|Release| |Python versions| |Downloads count| |Build status| |Test coverage| |Codacy Badge| |Documantation|

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

.. |Codacy Badge| image:: https://app.codacy.com/project/badge/Grade/19d5c531ed75435988ba8dc91031514c
  :target: https://www.codacy.com/gh/ri-gilfanov/aiohttp-sqlalchemy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ri-gilfanov/aiohttp-sqlalchemy&amp;utm_campaign=Badge_Grade
   :alt: Codacy Badge

.. |Documantation| image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation

`SQLAlchemy 1.4 / 2.0 <https://www.sqlalchemy.org/>`_ support for `AIOHTTP
<https://docs.aiohttp.org/>`_.

The library provides the next features:

* initializing asynchronous sessions through a middlewares;
* initializing asynchronous sessions through a decorators;
* simple access to one asynchronous session by default key;
* preventing attributes from being expired after commit by default;
* support different types of request handlers;
* support nested applications.


Installation
------------
Installing ``aiohttp-sqlalchemy`` with pip: ::

  pip install aiohttp-sqlalchemy


Optional requirements
---------------------

For PostgreSQL support, you also need install ``asyncpg``: ::

  pip install asyncpg

For MySQL support, you also need install ``aiomysql``: ::

  pip install aiomysql

For SQLite3 support, you also need install ``aiosqlite``: ::

  pip install aiosqlite


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


Multiple session factories in application
-----------------------------------------
.. code-block:: python

  import aiohttp_sqlalchemy

  postgresql_url = 'postgresql+asyncpg://user:password@host/database'
  mysql_url = 'mysql+aiomysql://user:password@host/database'
  sqlite_url = 'sqlite+aiosqlite:///path/to/file.sqlite3'

  aiohttp_sqlalchemy.setup(app, [
      aiohttp_sqlalchemy.bind(postgresql_url),
      aiohttp_sqlalchemy.bind(mysql_url, 'sa_second'),
      aiohttp_sqlalchemy.bind(sqlite_url, 'sa_third'),
  ])

Multiple database backends per session
--------------------------------------
See `Partitioning Strategies (e.g. multiple database backends per Session)
<https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session>`_
section in SQLAlchemy 1.4 documentation.

Class based views
-----------------
.. code-block:: python

  class Handler(aiohttp_sqlalchemy.SAView):
      async def get(self):
          db_session = self.sa_session()

          # some your code

  aiohttp_sqlalchemy.setup(app, [
      aiohttp_sqlalchemy.bind(MainSession),
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
      aiohttp_sqlalchemy.bind(Session, 'sa_optional', middleware=False),
  ])


Change log
----------
Version 0.16.1
^^^^^^^^^^^^^^
Added
"""""
* Added utility ``sa_session_factory(source, key = SA_DEFAULT_KEY)``, when
  ``source`` can be instance of ``aiohttp.web.Request`` or
  ``aiohttp.web.Application``.

Version 0.15.4
^^^^^^^^^^^^^^
Changed
"""""""
* Changed ``DEFAULT_KEY`` from deprecated to synonym.

Version 0.15
^^^^^^^^^^^^
Added
"""""
* Added synonym ``bind`` for ``sa_bind``.
* Added synonym ``init_db`` for ``sa_init_db``.

Version 0.14
^^^^^^^^^^^^
Added
"""""
* Added utility ``sa_init_db(app, metadata, key = SA_DEFAULT_KEY)``.
* Added constant ``SA_DEFAULT_KEY`` instead ``DEFAULT_KEY``.

Deprecated
""""""""""
* ``DEFAULT_KEY`` is deprecated. Use ``SA_DEFAULT_KEY``.

Version 0.13
^^^^^^^^^^^^
Changed
"""""""
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
