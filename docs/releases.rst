========
Releases
========
Unreleased
----------
**Added**

* Synonym ``SAView`` for ``SAModelView``.

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

* ``views.SAAbstractView`` synonym for ``views.SAMixin``;
* ``views.SAOneModelMixin`` synonym for ``views.SAModelMixin``;

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
  ``sessionmaker(engine, AsyncSession)`` or custom session factory returning
  ``AsyncSession`` instance.

Version 0.8
-----------
**Changed**

* Rename first argument from ``arg`` to ``factory`` in ``sa_bind()`` signature.

**Deprecated**

* ``AsyncEngine`` type is deprecated in ``sa_bind()`` signature. Use
  ``sessionmaker(engine, AsyncSession)`` or custom session factory returning
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
