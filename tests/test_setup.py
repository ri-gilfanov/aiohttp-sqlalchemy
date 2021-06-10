from aiohttp import web
import pytest

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import DuplicateAppKeyError, sa_bind


async def test_duplicate_app_key_error(orm_session_factory):

    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(web.Application(), [
            sa_bind(orm_session_factory),
            sa_bind(orm_session_factory),
        ])

    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(web.Application(), [
            sa_bind(orm_session_factory, 'sa_secondary'),
            sa_bind(orm_session_factory, 'sa_secondary'),
        ])

    aiohttp_sqlalchemy.setup(web.Application(), [
        sa_bind(orm_session_factory),
        sa_bind(orm_session_factory, 'sa_secondary'),
    ])
