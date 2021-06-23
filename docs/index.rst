==================================
aiohttp-sqlalchemy's documentation
==================================
|Python versions| |PyPI release| |PyPI downloads| |License| |ReadTheDocs| |GitHub CI| |Codecov| |Codacy|

.. |Python versions| image:: https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Python version support

.. |PyPI release| image:: https://badge.fury.io/py/aiohttp-sqlalchemy.svg
  :target: https://pypi.org/project/aiohttp-sqlalchemy/
  :alt: Release

.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/aiohttp-sqlalchemy
  :target: https://pypistats.org/packages/aiohttp-sqlalchemy
  :alt: PyPI downloads count

.. |License| image:: https://img.shields.io/badge/License-BSD-green
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/blob/master/LICENSE
  :alt: BSD 3-Clause "New" or "Revised" License

.. |ReadTheDocs| image:: https://readthedocs.org/projects/aiohttp-sqlalchemy/badge/?version=latest
  :target: https://aiohttp-sqlalchemy.readthedocs.io/en/latest/?badge=latest
  :alt: Read The Docs build

.. |GitHub CI| image:: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml/badge.svg?branch=master
  :target: https://github.com/ri-gilfanov/aiohttp-sqlalchemy/actions/workflows/ci.yml
  :alt: GitHub continuous integration

.. |Codecov| image:: https://codecov.io/gh/ri-gilfanov/aiohttp-sqlalchemy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ri-gilfanov/aiohttp-sqlalchemy
  :alt: codecov.io status for master branch

.. |Codacy| image:: https://app.codacy.com/project/badge/Grade/19d5c531ed75435988ba8dc91031514c
  :target: https://www.codacy.com/gh/ri-gilfanov/aiohttp-sqlalchemy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ri-gilfanov/aiohttp-sqlalchemy&amp;utm_campaign=Badge_Grade
   :alt: Codacy code quality

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
