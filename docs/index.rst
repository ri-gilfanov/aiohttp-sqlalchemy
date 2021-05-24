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


Overview
--------

SQLAlchemy 1.4 / 2.0 support for aiohttp.

By default, library forwards:

* ``sqlalchemy.ext.asyncio.AsyncSession`` object as ``request['sa_main']``
  or ``SAView.sa_main_session``
* ``sqlalchemy.ext.asyncio.AsyncEngine`` object as ``request.app['sa_main']``


Installation
------------
::

    pip install aiohttp-sqlalchemy


Simple example
--------------
Install aiosqlite for work with sqlite3: ::

  pip install aiosqlite

Copy and paste this code in a file and run:

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_engine, sa_middleware
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
       async with request.app['sa_main'].begin() as conn:
           await conn.run_sync(Base.metadata.create_all)

       async with request['sa_main'].begin():
           request['sa_main'].add_all([MyModel()])
           result = await request['sa_main'].execute(sa.select(MyModel))
           data = {r.id: r.timestamp.isoformat() for r in result.scalars()}
           return web.json_response(data)


   app = web.Application()

   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])

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
      sa_engine(main_engine),
      sa_engine(second_engine, 'sa_second'),
      sa_engine(third_engine, 'sa_third'),
  ])


Class based views
-----------------
.. warning::

   For use a ``SAView`` in class based view inheritance, you must bind an
   ``AsyncEngine`` with default key.

.. code-block:: python

   from aiohttp_sqlalchemy import SAView

   class Handler(SAView):
       async def get(self):
           async with sa_main_session.begin():
               # some your code

   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])


Decorating handlers
-------------------
.. warning::

   For use a some ``AsyncEngine`` in decorators, you must set a ``middleware``
   argument to ``False`` in ``sa_engine`` call. Else will raise an exception
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
       sa_engine(engine, 'sa_fourth', middleware=False),
   ])


Nested apps
-----------
If you need access to ``AsyncEngine`` object from nested app, then you must
use ``request.config_dict.get()`` method.

Access to ``AsyncSession`` object from nested app has no differences.

.. code-block:: python

   async def main(request):
       async with request.config_dict.get('sa_main').begin() as conn:
           # some operations with AsyncEngine object

       async with request['sa_main'].begin():
           # some operations with AsyncSession object

   app = web.Application()

   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])

   subapp = web.Application()
   subapp.add_routes([web.get('', main)])

   app.add_subapp(prefix='/subapp', subapp=subapp)



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
