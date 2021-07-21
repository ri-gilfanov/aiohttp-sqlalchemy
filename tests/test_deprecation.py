import pytest


def test_deprecation() -> None:
    from aiohttp_sqlalchemy import views
    from aiohttp_sqlalchemy import web_handlers
    assert views is web_handlers

    from aiohttp_sqlalchemy import SAItemAddMixin
    from aiohttp_sqlalchemy import ItemAddMixin
    assert SAItemAddMixin is ItemAddMixin

    from aiohttp_sqlalchemy.web_handlers import SAListAddMixin
    from aiohttp_sqlalchemy.web_handlers import ListAddMixin
    assert SAListAddMixin is ListAddMixin

    with pytest.raises(ImportError):
        from aiohttp_sqlalchemy import NotExist
        assert bool(NotExist)
