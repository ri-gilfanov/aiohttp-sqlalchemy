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
.. warning::

  API of most classes of stabilizes to version 1.0.

.. autoclass:: aiohttp_sqlalchemy.SAMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelMixin
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelViewMixin
  :inherited-members:
  :members:
  :show-inheritance:

Instance mixins
^^^^^^^^^^^^^^^
.. autoclass:: aiohttp_sqlalchemy.PrimaryKeyMixin
  :inherited-members:
  :members:
  :show-inheritance:

  .. autoclass:: aiohttp_sqlalchemy.ItemAddMixin
    :inherited-members:
    :members:
    :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ItemDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ItemEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ItemViewMixin
  :inherited-members:
  :members:
  :show-inheritance:

List mixins
^^^^^^^^^^^
.. autoclass:: aiohttp_sqlalchemy.OffsetPagination
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ListAddMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ListDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ListEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.ListViewMixin
  :inherited-members:
  :members:
  :show-inheritance:

Views
^^^^^
.. autoclass:: aiohttp_sqlalchemy.SABaseView
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelView
  :members:
  :show-inheritance:

Additional functionality
------------------------
.. autofunction:: aiohttp_sqlalchemy.sa_decorator

.. autofunction:: aiohttp_sqlalchemy.sa_middleware

.. autofunction:: aiohttp_sqlalchemy.get_session_factory
