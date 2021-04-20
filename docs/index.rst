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

SQLAlchemy >= 1.4 support for aiohttp.

Install
-------
::

   pip install aiohttp-sqlalchemy


Middleware approach
-------------------
Using middlewares is preferred for most users.

Single middleware
'''''''''''''''''

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_engine, sa_middleware

   async def main(request):
       async with request['sa_main'].begin():
            # some code

   app = web.Application(middlewares=[sa_middleware()])
   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])


Multiple middlewares
''''''''''''''''''''

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_engine, sa_middleware

   async def main(request):
       async with request['sa_main'].begin():
            # some code

       async with request['sa_secondary'].begin():
            # some code

   app = web.Application(middlewares=[
       sa_middleware(),
       sa_middleware('sa_secondary')])
   main_engine = create_async_engine('sqlite+aiosqlite:///')
   secondary_engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [
        sa_engine(main_engine),
        sa_engine(secondary_engine, 'sa_secondary'),
   ])


Decorator approach
------------------
But you can use decorators instead of middlewares.

Decorated coroutine function
''''''''''''''''''''''''''''

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_decorator, sa_engine, sa_middleware

   @sa_decorator()
   async def main(request):
       async with request['sa_main'].begin():
            # some code

   app = web.Application()
   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])

Decorated class based view
''''''''''''''''''''''''''

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_decorator, sa_engine, sa_middleware

   class ClassBasedView(web.View):
       @sa_decorator()
       async def get(self):
            async with request['sa_main'].begin():
                # some code

   app = web.Application()
   engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [sa_engine(engine)])


Hybrid approach
---------------
And you can combine the middleware approach and the decorator approach.

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_decorator, sa_engine, sa_middleware
   from sqlalchemy.ext.asyncio import create_async_engine

   @sa_decorator('sa_secondary')
   async def main(request):
        # some your code

   app = web.Application(middlewares=[
       sa_middleware(),
   ])
   main_engine = create_async_engine('sqlite+aiosqlite:///')
   secondary_engine = create_async_engine('sqlite+aiosqlite:///')
   aiohttp_sqlalchemy.setup(app, [
        sa_engine(main_engine),
        sa_engine(secondary_engine, 'sa_secondary'),
   ])


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
