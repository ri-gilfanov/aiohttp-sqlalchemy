==================
aiohttp-sqlalchemy
==================
|ReadTheDocs| |PyPI release| |PyPI downloads| |Python versions| |License| |GitHub CI| |Codecov| |Codacy|

.. |ReadTheDocs| image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Read The Docs build

.. |PyPI release| image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Release

.. |PyPI downloads| image:: https://static.pepy.tech/personalized-badge/aiohttp-sqlalchemy?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads
  :target: https://pepy.tech/project/aiohttp-sqlalchemy
  :alt: PyPI downloads count

.. |Python versions| image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Python version support

.. |License| image:: https://img.shields.io/badge/License-MIT-green
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/blob/master/LICENSE
  :alt: MIT License

.. |GitHub CI| image:: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml/badge.svg?branch=master
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml
  :alt: GitHub continuous integration

.. |Codecov| image:: https://codecov.io/gh/ri-gilfanov/aiohttp-sqlalchemy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ri-gilfanov/aiohttp-sqlalchemy
  :alt: codecov.io status for master branch

.. |Codacy| image:: https://app.codacy.com/project/badge/Grade/19d5c531ed75435988ba8dc91031514c
  :target: https://www.codacy.com/gh/ri-gilfanov/aiohttp-sqlalchemy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ri-gilfanov/aiohttp-sqlalchemy&amp;utm_campaign=Badge_Grade
   :alt: Codacy code quality

`SQLAlchemy 2.0 <https://www.sqlalchemy.org/>`_ support for `AIOHTTP
<https://docs.aiohttp.org/>`_.

The library provides the next features:

* initializing asynchronous sessions through a middlewares;
* initializing asynchronous sessions through a decorators;
* simple access to one asynchronous session by default key;
* preventing attributes from being expired after commit by default;
* support different types of request handlers;
* support nested applications.


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

  from datetime import datetime

  import sqlalchemy as sa
  from aiohttp import web
  from sqlalchemy import orm

  import aiohttp_sqlalchemy as ahsa

  metadata = sa.MetaData()
  Base = orm.declarative_base(metadata=metadata)


  class MyModel(Base):
      __tablename__ = 'my_table'

      pk = sa.Column(sa.Integer, primary_key=True)
      timestamp = sa.Column(sa.DateTime(), default=datetime.now)


  async def main(request):
      sa_session = ahsa.get_session(request)

      async with sa_session.begin():
          sa_session.add(MyModel())
          result = await sa_session.execute(sa.select(MyModel))
          result = result.scalars()

      data = {
          instance.pk: instance.timestamp.isoformat()
          for instance in result
      }
      return web.json_response(data)


  async def app_factory():
      app = web.Application()

      ahsa.setup(app, [
          ahsa.bind('sqlite+aiosqlite:///'),
      ])
      await ahsa.init_db(app, metadata)

      app.add_routes([web.get('/', main)])
      return app


  if __name__ == '__main__':
      web.run_app(app_factory())
