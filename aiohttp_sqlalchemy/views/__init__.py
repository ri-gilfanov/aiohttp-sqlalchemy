from aiohttp.web import View
from aiohttp_sqlalchemy.views.mixins import SAViewMixin


class SAView(View, SAViewMixin):
    """ SQLAlchemy class based view. """
    pass
