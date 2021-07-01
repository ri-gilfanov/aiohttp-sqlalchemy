==============
Advansed usage
==============
Multiple database backends per session
--------------------------------------
See `Partitioning Strategies (e.g. multiple database backends per Session)
<https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#partitioning-strategies-e-g-multiple-database-backends-per-session>`_
section in SQLAlchemy 1.4 documentation.

Multiple session factories in application
-----------------------------------------
.. code-block:: python

  import aiohttp_sqlalchemy as ahsa

  postgresql_url = 'postgresql+asyncpg://user:password@host/database'
  mysql_url = 'mysql+aiomysql://user:password@host/database'
  sqlite_url = 'sqlite+aiosqlite:///path/to/file.sqlite3'

  ahsa.setup(app, [
      ahsa.bind(postgresql_url),
      ahsa.bind(mysql_url, 'sa_second'),
      ahsa.bind(sqlite_url, 'sa_third'),
  ])


Decorating handlers
-------------------
.. warning::

  For use a some session factory in decorators, you must set a ``middleware``
  argument to ``False`` in ``bind()`` call. Else will raise an exception
  ``DuplicateRequestKeyError``.

If access to one or more databases is needed only in some request handlers, then you can
use a ``sa_decorator(key)``. For example:

.. code-block:: python

  import aiohttp_sqlalchemy as ahsa

  @ahsa.sa_decorator('sa_specific')
  async def specific_handler(request):
      specific_db_session = ahsa.get_session(request, 'sa_specific')

      async with specific_db_session.begin():
          # some your code

  ahsa.setup(app, [
      ahsa.bind(specific_db_url, 'sa_specific', middleware=False),
  ])

You can combine the use of decorators with the use of middlewares. For example:

.. code-block:: python

  import aiohttp_sqlalchemy as ahsa

  async def simple_handler(request):
      main_db_session = ahsa.get_session(request)

      async with main_db_session.begin():
          # some your code


  @ahsa.sa_decorator('sa_specific')
  async def specific_handler(request):
      main_db_session = ahsa.get_session(request)
      specific_db_session = ahsa.get_session(request, 'sa_specific')

      async with main_db_session.begin():
          # some your code

      async with specific_db_session.begin():
          # some your code


  ahsa.setup(app, [
      ahsa.bind(main_db_url),
      ahsa.bind(specific_db_url, 'sa_specific', middleware=False),
  ])
  app.add_routes([
      web.get('/simple', simple_handler),
      web.get('/specific', specific_handler),
  ])

You can apply ``sa_decorator(key)`` with class based views. For example:

.. code-block:: python

  from aiohttp import web
  import aiohttp_sqlalchemy as ahsa


  SPECIFIC_DB_KEY = 'sa_specific'
  SPECIFIC_DB_URL = 'sqlite+aiosqlite:///'


  class SpecificHandler(ahsa.SABaseView):
      @property
      def specific_session(self):
          return self.sa_session(SPECIFIC_DB_KEY)

      @ahsa.sa_decorator(SPECIFIC_DB_KEY)
      async def get(self):
          async with self.specific_session.begin():
              # some your code

      @ahsa.sa_decorator(SPECIFIC_DB_KEY)
      async def post(self):
          async with self.specific_session.begin():
              # some your code


  ahsa.setup(app, [
      ahsa.bind(SPECIFIC_DB_URL, SPECIFIC_DB_KEY, middleware=False),
  ])
  app.add_routes([web.view('/', SpecificHandler)])
