==================
aiohttp-sqlalchemy
==================

SQLAlchemy >= 1.4 support for aiohttp.

Install
-------
::

    pip install aiohttp-sqlalchemy


Example
-------

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

Documentation
-------------

See: https://aiohttp-sqlalchemy.readthedocs.io/

