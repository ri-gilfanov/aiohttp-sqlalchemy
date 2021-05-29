from aiohttp.abc import AbstractView
from aiohttp_sqlalchemy.views.mixins import SAViewMixin


class AbstractSAView(AbstractView, SAViewMixin):
    """ SQLAlchemy abstract class based view mixin. """
