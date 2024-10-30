========
Releases
========
Version 1.0.1
-------------

**Added**

* Added support for Python 3.13.

**Changed**

* Update dependencies.

Version 1.0.post0
-----------------
**Changed**

* ``sessionmaker`` replaced on ``async_sessionmaker``.

Version 1.0.0
-------------
**Added**

* Added support for SQLAlchemy 2.0.

**Removed**

* Dropped support for SQLAlchemy 1.4.

Version 0.35
------------
**Added**

* Added support for Python 3.11 and 3.12.

**Changed**

* Hold aiohttp-things and sqlalchemy-things versions.

**Removed**

* Dropped support for Python 3.7.

Version 0.34
------------
**Added**

* Add official support Python 3.10;
* Add ``get_engine`` util.

**Changed**

* Argument ``target`` in signature ``bind(target ,key=SA_DEFAULT_KEY, *,
  middleware=True)`` can be of the following types ``str``,
  ``sqlalchemy.ext.asyncio.AsyncEngine``, ``sqlalchemy.orm.sessionmaker``
  or their compatible descendants. Custom session factory is no longer
  supported.

**Removed**

* Removed ``views`` synonym for ``web_handlers``;
* Removed ``ItemAddMixin`` synonym for ``UnitAddMixin``;
* Removed ``ItemDeleteMixin`` synonym for ``UnitDeleteMixin``;
* Removed ``ItemEditMixin`` synonym for ``UnitEditMixin``;
* Removed ``ItemViewMixin`` synonym for ``UnitViewMixin``;
* Removed ``OffsetPagination`` synonym for ``OffsetPaginationMixin``;
* Removed ``SAItemAddMixin`` synonym for ``UnitAddMixin``;
* Removed ``SAItemDeleteMixin`` synonym for ``UnitDeleteMixin``;
* Removed ``SAItemEditMixin`` synonym for ``UnitEditMixin``;
* Removed ``SAItemViewMixin`` synonym for ``UnitViewMixin``;
* Removed ``SAListAddMixin'`` synonym for ``ListAddMixin``;
* Removed ``SAListDeleteMixin`` synonym for ``ListDeleteMixin``;
* Removed ``SAListEditMixin`` synonym for ``ListEditMixin``;
* Removed ``SAListViewMixin`` synonym for ``ListViewMixin``;
* Removed ``SAModelDeleteMixin`` synonym for ``DeleteStatementMixin``;
* Removed ``SAModelEditMixin`` synonym for ``UpdateStatementMixin``;
* Removed ``SAModelViewMixin`` synonym for ``SelectStatementMixin``;
* Removed ``SAPrimaryKeyMixin`` synonym for ``PrimaryKeyMixin``.

Version 0.33
------------
* ``ItemAddMixin`` is deprecated. Use ``UnitAddMixin``;
* ``ItemDeleteMixin`` is deprecated. Use ``UnitDeleteMixin``;
* ``ItemEditMixin`` is deprecated. Use ``UnitEditMixin``;
* ``ItemViewMixin`` is deprecated. Use ``UnitViewMixin``.


Version 0.32
------------
* Added ``prepare_context()`` method for ``OffsetPaginationMixin``.


Version 0.31
------------
**Added**

* Added default ``page_key`` and ``page_key_adapter`` attributes
  for ``OffsetPaginationMixin``;
* Added ``execute_select_stmt()`` method for ``OffsetPaginationMixin``.

**Deprecated**

* ``OffsetPagination`` is deprecated. Use ``OffsetPaginationMixin``;
* ``SAModelDeleteMixin`` is deprecated. Use ``DeleteStatementMixin``;
* ``SAModelEditMixin`` is deprecated. Use ``UpdateStatementMixin``;
* ``SAModelViewMixin`` is deprecated. Use ``SelectStatementMixin``.

Version 0.30
------------
**Deprecated**

* ``views`` module is deprecated. Use import from ``aiohttp_sqlalchemy``
  or ``aiohttp_sqlalchemy.web_handlers``;
* ``SAItemAddMixin`` synonym is deprecated. Use ``ItemAddMixin`` class;
* ``SAItemDeleteMixin`` is deprecated. Use ``ItemDeleteMixin`` class;
* ``SAItemEditMixin`` synonym is deprecated. Use ``ItemEditMixin`` class;
* ``SAItemViewMixin`` synonym is deprecated. Use ``ItemViewMixin`` class;
* ``SAListAddMixin`` synonym is deprecated. Use ``ListAddMixin`` class;
* ``SAListDeleteMixin`` synonym is deprecated. Use ``ListDeleteMixin`` class;
* ``SAListEditMixin`` synonym is deprecated. Use ``ListEditMixin`` class;
* ``SAListViewMixin`` synonym is deprecated. Use ``ListViewMixin`` class;
* ``SAPrimaryKeyMixin`` synonym is deprecated. Use ``PrimaryKeyMixin`` class.

Version 0.29
------------
**Added**

* ``OffsetPagination``.

**Changed**

* ``SAListViewMixin`` class is no longer inherited from
  ``aiohttp_things.PaginationMixin``.

Version 0.28
------------
**Changed**

* Renamed ``handlers`` module to ``web_handlers``;
* Renamed ``sa_session`` method to ``get_sa_session`` in ``SAMixin``;
* Renamed ``get_sa_delete_stmt`` method to ``get_delete_stmt``
  in ``SAModelDeleteMixin`` and ``ItemDeleteMixin``;
* Renamed ``get_sa_update_stmt`` method to ``get_update_stmt``
  in ``SAModelEditMixin`` and ``ItemEditMixin``;
* Renamed ``get_sa_view_stmt`` method to ``get_select_stmt``
  in ``SAModelViewMixin`` and ``ItemViewMixin``.

Version 0.27
------------
**Added**

* ``SAItemAddMixin`` as a synonym for ``ItemAddMixin``;
* ``SAItemDeleteMixin`` as a synonym for ``ItemDeleteMixin``;
* ``SAItemEditMixin`` as a synonym for ``ItemEditMixin``;
* ``SAItemViewMixin`` as a synonym for ``ItemViewMixin``;
* ``SAListAddMixin`` as a synonym for ``ListAddMixin``;
* ``SAListDeleteMixin`` as a synonym for ``ListDeleteMixin``;
* ``SAListEditMixin`` as a synonym for ``ListEditMixin``;
* ``SAListViewMixin`` as a synonym for ``ListViewMixin``;
* ``SAPrimaryKeyMixin`` as a synonym for ``PrimaryKeyMixin``.

**Changed**

* ``views`` module renamed to ``handlers``;
* classes from ``handlers`` temporarily imported to empty ``views`` module for
  backward compatibility;
* ``SAItemAddMixin`` renamed to ``ItemAddMixin``;
* ``SAItemDeleteMixin`` renamed to ``ItemDeleteMixin``;
* ``SAItemEditMixin`` renamed to ``ItemEditMixin``;
* ``SAItemViewMixin`` renamed to ``ItemViewMixin``;
* ``SAListAddMixin`` renamed to ``ListAddMixin``;
* ``SAListDeleteMixin`` renamed to ``ListDeleteMixin``;
* ``SAListEditMixin`` renamed to ``ListEditMixin``;
* ``SAListViewMixin`` renamed to ``ListViewMixin``;
* ``SAPrimaryKeyMixin`` renamed to ``PrimaryKeyMixin``.

**Removed**

* ``SAView`` a synonym for ``SAModelView``.

Version 0.26
------------
**Changed**

* ``SAListViewMixin`` inherited by ``aiohttp_things.PaginationMixin``.

**Removed**

* ``SAListMixin`` class removed, use ``aiohttp_things.ListMixin``;
* ``SAItemMixin`` class removed, use ``aiohttp_things.ItemMixin``.

Version 0.25
------------
**Changed**

* Attribute ``instance`` renamed to ``item`` in ``SAItemAddMixin``,
  ``SAItemEditMixin``, ``SAItemViewMixin``.

**Removed**

* ``SAInstanceMixin`` removed, use ``SAItemMixin``.

Version 0.24
------------
**Removed**

* ``SAInstanceView`` class;
* ``SAItemView`` synonym for ``SAInstanceView``;
* ``SAAbstractView`` synonym for ``SAMixin``;
* ``SAOneModelMixin`` synonym for ``SAModelMixin``;
* ``SAInstanceAddMixin`` synonym for ``SAItemAddMixin``;
* ``SAInstanceDeleteMixin`` synonym for ``SAItemDeleteMixin``;
* ``SAInstanceEditMixin`` synonym for ``SAItemEditMixin``;
* ``SAInstanceViewMixin`` synonym for ``SAItemViewMixin``.

Version 0.23
------------
**Add**

* ``SAItemMixin`` as a separate mixin;
* ``SAInstanceAddMixin`` as a synonym for ``SAItemAddMixin``;
* ``SAInstanceDeleteMixin`` as a synonym for ``SAItemDeleteMixin``;
* ``SAInstanceEditMixin`` as a synonym for ``SAItemEditMixin``;
* ``SAInstanceViewMixin`` as a synonym for ``SAItemViewMixin``;

**Changed**

* ``SAInstanceAddMixin`` renamed to ``SAItemAddMixin``;
* ``SAInstanceDeleteMixin`` renamed to ``SAItemDeleteMixin``;
* ``SAInstanceEditMixin`` renamed to ``SAItemEditMixin``;
* ``SAInstanceViewMixin`` renamed to ``SAItemViewMixin``;
* ``SAItemMixin`` is no longer a synonym for ``SAInstanceMixin``.

Version 0.22
------------
**Added**

* ``SAModelDeleteMixin``;
* ``SAModelEditMixin``;
* ``SAModelViewMixin``;
* ``SAPrimaryKeyMixin``;
* ``SAInstanceAddMixin``;
* ``SAInstanceDeleteMixin``;
* ``SAInstanceEditMixin``;
* ``SAInstanceViewMixin``;
* ``SAListMixin``;
* ``SAListAddMixin``;
* ``SAListDeleteMixin``;
* ``SAListEditMixin``;
* ``SAListViewMixin``.

Version 0.21
------------
**Changed**

* Rename ``SAItemMixin`` to ``SAInstanceMixin``;
* Rename ``SAItemView`` to ``SAInstanceView``.

**Added**

* ``SAItemMixin`` as a synonym for ``SAInstanceMixin``;
* ``SAItemView`` as a synonym for ``SAInstanceView``.

Version 0.20
------------
**Added**

* Added ``SAItemMixin``;
* Added ``SAItemView``.

Version 0.19
------------
**Added**

* ``sa_session`` as a synonym for ``get_session``;
* ``sa_session_factory`` as a synonym for ``get_session_factory``.

**Changed**

* Rename ``sa_session`` to ``get_session``;
* Rename ``sa_session_factory`` to ``get_session_factory``.

Version 0.18.1
--------------
**Added**

* ``SAView`` as a synonym for ``SAModelView``.

**Changed**

* Rename ``SAView`` to ``SAModelView``.

Version 0.18
------------
**Changed**

* First argument of function ``aiohttp_sqlalchemy.bind()`` renamed from
  ``bind_to`` to ``target``;
* Type hint alias ``TBinding`` renamed to ``TBind``;
* Type hint alias ``TBindings`` renamed to ``TBinds``;
* Type hint alias ``TBindTo`` renamed to ``TTarget``.

Version 0.17
------------
**Added**

* ``views.SAAbstractView`` as a synonym for ``views.SAMixin``;
* ``views.SAOneModelMixin`` as a synonym for ``views.SAModelMixin``;

**Changed**

* type checks in ``aiohttp_sqlalchemy.bind()``including replacing from ``ValueError``
  to ``TypeError``;
* ``views.SAAbstractView`` renamed ``views.SAMixin``;
* ``views.SAOneModelMixin`` renamed ``views.SAModelMixin``.

**Removed**

* Removed type check of result of call session factory.

Version 0.16
------------
**Added**

* Added utility ``sa_session_factory(source, key = SA_DEFAULT_KEY)``, when ``source``
  can be instance of ``aiohttp.web.Request`` or ``aiohttp.web.Application``.

Version 0.15.4
--------------
**Changed**

* Changed ``DEFAULT_KEY`` from deprecated to synonym.

Version 0.15
------------
**Added**

* Added synonym ``bind`` for ``sa_bind``;
* Added synonym ``init_db`` for ``sa_init_db``.

Version 0.14
------------
**Added**

* Added utility ``sa_init_db(app, metadata, key = SA_DEFAULT_KEY)``;
* Added constant ``SA_DEFAULT_KEY`` instead ``DEFAULT_KEY``.

**Deprecated**

* ``DEFAULT_KEY`` is deprecated. Use ``SA_DEFAULT_KEY``.

Version 0.13
------------
**Changed**

* Argument ``expire_on_commit`` of ``sessionmaker`` set to ``False``
  by default.

Version 0.12
------------
**Added**

* Added ``sa_session_key`` attribute in ``SAAbstractView`` class;
* Added support url and ``AssyncEngine`` instance as first argument in ``sa_bind()``.

**Changed**

* Rename first argument from ``factory`` to ``bind_to`` in ``sa_bind()`` signature.

Version 0.11
------------
**Added**

* Added ``sa_session(request, key='sa_main')`` utility.

Version 0.10
------------
**Added**

* Added support Python 3.7.

Version 0.9
-----------
**Added**

* Support of `organized handlers in class
  <https://docs.aiohttp.org/en/stable/web_quickstart.html#organizing-handlers-in-classes>`_
  added to ``sa_decorator(key)``.

**Removed**

* Removed support of ``AsyncEngine`` type in ``sa_bind()`` signature. Use
  ``async_sessionmaker(engine, AsyncSession)`` or custom session factory returning
  ``AsyncSession`` instance.

Version 0.8
-----------
**Changed**

* Rename first argument from ``arg`` to ``factory`` in ``sa_bind()`` signature.

**Deprecated**

* ``AsyncEngine`` type is deprecated in ``sa_bind()`` signature. Use
  ``async_sessionmaker(engine, AsyncSession)`` or custom session factory returning
  ``AsyncSession`` instance.

Version 0.7
-----------
**Changed**

* Usage ``sqlalchemy.orm.sessionmaker`` instance is recomended as a first argument
  for ``aiohttp_sqlalchemy.sa_bind()`` signature. See examples in documetation.

**Removed**

* Removed support of ``request.config_dict.get('sa_main')`` and
  ``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind`` expression.

Version 0.6
-----------
**Added**

* Add support ``sqlalchemy.orm.sessionmaker`` as a first argument in function
  ``sa_bind(arg, key, middleware)``.

**Changed**

* Argument ``engine: AsyncEngine`` changed to ``arg: Union[AsyncEngine, sessionmaker]``
  in ``sa_bind()`` signature.

**Deprecated**

* Deprecated support of ``request.config_dict.get('sa_main')`` and
  ``request.app['sa_main']`` expressions. Use a ``request['sa_main'].bind`` expression.

**Removed**

* Deprecated class ``views.SAViewMixin`` is removed. Use ``views.SAAbstractView``;
* Deprecated attribute ``SAView.sa_main_session`` is removed. Use method
  ``SAView.sa_session(key: str = 'sa_main')``.

Version 0.5
-----------
**Removed**

* Deprecated function ``aiohttp_sqlalchemy.sa_engine()`` is removed. Use
  ``aiohttp_sqlalchemy.sa_bind()``.

**Deprecated**

* Undocumented class ``views.SAViewMixin`` is deprecated. Use ``views.SAAbstractView``.

Version 0.4
-----------
**Added**

* ``SAView.sa_session(key: str = 'sa_main')`` function is added instead
  ``SAView.sa_main_session``.

**Deprecated**

* ``SAView.sa_main_session`` is deprecated. Use
  ``SAView.sa_session(key: str = 'sa_main')``.

Version 0.3
-----------
**Added**

* ``aiohttp_sqlalchemy.sa_bind()`` function is added instead
  ``aiohttp_sqlalchemy.sa_engine()``.

**Deprecated**

* ``aiohttp_sqlalchemy.sa_engine()`` function is deprecated. Use
  ``aiohttp_sqlalchemy.sa_bind()``.
