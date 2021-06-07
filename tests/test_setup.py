from aiohttp import web
import pytest

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import sa_bind
from aiohttp_sqlalchemy.exceptions import DuplicateAppKeyError


async def test_duplicate_app_key_error(sa_session_factory):

    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(web.Application(), [
            sa_bind(sa_session_factory),
            sa_bind(sa_session_factory),
        ])

    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(web.Application(), [
            sa_bind(sa_session_factory, 'sa_secondary'),
            sa_bind(sa_session_factory, 'sa_secondary'),
        ])

    aiohttp_sqlalchemy.setup(web.Application(), [
        sa_bind(sa_session_factory),
        sa_bind(sa_session_factory, 'sa_secondary'),
    ])
