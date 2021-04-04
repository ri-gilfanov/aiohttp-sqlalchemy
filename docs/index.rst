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


Single middleware
-----------------

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_engine, sa_middleware

   routes = web.RouteTableDef()

   @routes.get('/')
   async def main(request):
      async with request['sa_main'].begin():
         # some code

   app = web.Application(middlewares=[sa_middleware()])
   aiohttp_sqlalchemy.setup(app, [sa_engine('sqlite+aiosqlite:///')])
   app.add_routes(routes)
   web.run_app(app)


Multiple middlewares
--------------------

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_engine, sa_middleware

   routes = web.RouteTableDef()

   @routes.get('/')
   async def main(request):
      async with request['sa_primary'].begin():
         # some code

      async with request['sa_secondary'].begin():
         # some code

   middlewares = [sa_middleware('sa_primary'), sa_middleware('sa_secondary')]
   app = web.Application(middlewares=middlewares)
   aiohttp_sqlalchemy.setup(app, [
      sa_engine('sa_primary', 'sqlite+aiosqlite:///'),
      sa_engine('sa_secondary', 'sqlite+aiosqlite:///'),
   ])
   app.add_routes(routes)
   web.run_app(app)


Decorators instead middlewares
------------------------------

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_decorator, sa_engine, sa_middleware

   routes = web.RouteTableDef()

   @routes.get('/')
   @sa_decorator()
   async def main(request):
      async with request['sa_main'].begin():
         # some code

   @routes.view('/other_url')
   @sa_decorator()
   class ClassBasedView(web.View):
      async def get(self):
         async with request['sa_main'].begin():
            # some code

   app = web.Application()
   aiohttp_sqlalchemy.setup(app, [sa_engine('sqlite+aiosqlite:///')])
   app.add_routes(routes)
   web.run_app(app)


Hybrid approach
---------------

.. code-block:: python

   from aiohttp import web
   import aiohttp_sqlalchemy
   from aiohttp_sqlalchemy import sa_decorator, sa_engine, sa_middleware

   routes = web.RouteTableDef()

   @routes.get('/')
   async def main(request):
      async with request['sa_main'].begin():
         # some code

   @routes.view('/url_2')
   class ClassBasedView(web.View):
      async def get(self):
         async with request['sa_secondary'].begin():
            # some code

   @routes.get('/url_3')
   @sa_decorator('sa_tertiary')
   async def main(request):
      async with request['sa_tertiary'].begin():
         # some code

   middlewares = [sa_middleware(), sa_middleware('sa_secondary')]

   app = web.Application(middlewares=middlewares)
   aiohttp_sqlalchemy.setup(app, [
      sa_engine('sqlite+aiosqlite:///'),
      sa_engine('sa_secondary', 'sqlite+aiosqlite:///'),
      sa_engine('sa_tertiary', 'sqlite+aiosqlite:///'),
   ])
   aiohttp_sqlalchemy.setup(app, [sa_engine('sqlite+aiosqlite:///')])
   app.add_routes(routes)
   web.run_app(app)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
