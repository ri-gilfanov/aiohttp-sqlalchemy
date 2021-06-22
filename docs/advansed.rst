==============
Advansed usage
==============
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

  For use a some session factory in decorators, you must set a ``middleware``
  argument to ``False`` in ``bind()`` call. Else will raise an exception
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
