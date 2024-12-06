==================================
aiohttp-sqlalchemy's documentation
==================================
|ReadTheDocs| |PyPI release| |License| |Python versions| |PyPI downloads| |GitHub CI|

.. |ReadTheDocs| image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Read The Docs build

.. |PyPI release| image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Release

.. |PyPI downloads| image:: https://static.pepy.tech/personalized-badge/aiohttp-sqlalchemy?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads
  :target: https://pepy.tech/project/aiohttp-sqlalchemy
  :alt: PyPI downloads count

.. |Python versions| image:: https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Python version support

.. |License| image:: https://img.shields.io/badge/License-MIT-green
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/blob/master/LICENSE
  :alt: MIT License

.. |GitHub CI| image:: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml/badge.svg?branch=master
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml
  :alt: GitHub continuous integration

`SQLAlchemy 2.0 <https://www.sqlalchemy.org/>`_ support for `AIOHTTP
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

  installation
  quickstart
  advansed
  reference
  releases
