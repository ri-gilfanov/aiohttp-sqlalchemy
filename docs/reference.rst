=========
Reference
=========
Main user functionality
-----------------------
.. autofunction:: aiohttp_sqlalchemy.setup

.. autofunction:: aiohttp_sqlalchemy.bind

.. autofunction:: aiohttp_sqlalchemy.init_db

.. autofunction:: aiohttp_sqlalchemy.get_session

Class based views
-----------------
.. autoclass:: aiohttp_sqlalchemy.SAMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelMixin
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAItemMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SABaseView
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelView
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAItemView
  :members:
  :show-inheritance:

Additional functionality
------------------------
.. autofunction:: aiohttp_sqlalchemy.sa_decorator

.. autofunction:: aiohttp_sqlalchemy.sa_middleware

.. autofunction:: aiohttp_sqlalchemy.get_session_factory
