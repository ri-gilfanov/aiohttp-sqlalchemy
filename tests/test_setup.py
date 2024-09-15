from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from aiohttp import web

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.orm import Session, sessionmaker


import aiohttp_sqlalchemy
from aiohttp_sqlalchemy import DuplicateAppKeyError


async def test_duplicate_app_key_error(
    session_factory: sessionmaker[Session],
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
