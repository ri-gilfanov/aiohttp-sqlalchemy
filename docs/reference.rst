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

  The API of class based views is experimental and unstable.

.. autoclass:: aiohttp_sqlalchemy.SAMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SAModelMixin
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.DeleteStatementMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.UpdateStatementMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.SelectStatementMixin
  :inherited-members:
  :members:
  :show-inheritance:

Instance mixins
^^^^^^^^^^^^^^^
.. autoclass:: aiohttp_sqlalchemy.PrimaryKeyMixin
  :inherited-members:
  :members:
  :show-inheritance:

  .. autoclass:: aiohttp_sqlalchemy.UnitAddMixin
    :inherited-members:
    :members:
    :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.UnitDeleteMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.UnitEditMixin
  :inherited-members:
  :members:
  :show-inheritance:

.. autoclass:: aiohttp_sqlalchemy.UnitViewMixin
  :inherited-members:
  :members:
  :show-inheritance:

List mixins
^^^^^^^^^^^
.. autoclass:: aiohttp_sqlalchemy.OffsetPaginationMixin
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
