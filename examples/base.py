from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy import orm

if TYPE_CHECKING:
    from typing import Any


metadata = sa.MetaData()
Base: "Any" = orm.declarative_base(metadata=metadata)
DB_URL = "sqlite+aiosqlite:///"


class MyModel(Base):
    __tablename__ = "my_table"
    pk = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime(), default=datetime.now)
