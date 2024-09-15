import pytest
from aiohttp import web
from sqlalchemy.orm import sessionmaker

import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import DuplicateAppKeyError


async def test_duplicate_app_key_error(
    session_factory: sessionmaker,
) -> None:
    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(
            web.Application(),
            [
                aiohttp_sqlalchemy.bind(session_factory),
                aiohttp_sqlalchemy.bind(session_factory),
            ],
        )

    with pytest.raises(DuplicateAppKeyError):
        aiohttp_sqlalchemy.setup(
            web.Application(),
            [
                aiohttp_sqlalchemy.bind(session_factory, "sa_secondary"),
                aiohttp_sqlalchemy.bind(session_factory, "sa_secondary"),
            ],
        )

    aiohttp_sqlalchemy.setup(
        web.Application(),
        [
            aiohttp_sqlalchemy.bind(session_factory),
            aiohttp_sqlalchemy.bind(session_factory, "sa_secondary"),
        ],
    )
