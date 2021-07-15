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
.. autoclass:: aiohttp_sqlalchemy.SAInstanceMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAPrimaryKeyMixin
  :inherited-members:
  :members:
  :show-inheritance:

  .. autoclass:: aiohttp_sqlalchemy.SAItemAddMixin
    :inherited-members:
    :members:
    :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAItemDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAItemEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAItemViewMixin
  :inherited-members:
  :members:
  :show-inheritance:

List mixins
^^^^^^^^^^^
.. autoclass:: aiohttp_sqlalchemy.SAListMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAListAddMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAListDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAListEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAListViewMixin
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

.. autoclass:: aiohttp_sqlalchemy.SAInstanceView
  :members:
  :show-inheritance:

Additional functionality
------------------------
.. autofunction:: aiohttp_sqlalchemy.sa_decorator

.. autofunction:: aiohttp_sqlalchemy.sa_middleware

.. autofunction:: aiohttp_sqlalchemy.get_session_factory
