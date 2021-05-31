from abc import ABC
from aiohttp.abc import AbstractView
from aiohttp_sqlalchemy.views.mixins import SAViewMixin


class AbstractSAView(ABC, AbstractView, SAViewMixin):
    """ SQLAlchemy abstract class based view mixin. """
