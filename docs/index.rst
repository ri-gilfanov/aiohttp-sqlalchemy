==================================
aiohttp-sqlalchemy's documentation
==================================
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

.. toctree::
  :maxdepth: 1
  :caption: Contents

  quickstart
  advansed
  reference
  releases
