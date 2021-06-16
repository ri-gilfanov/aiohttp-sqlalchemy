from aiohttp_sqlalchemy import SA_DEFAULT_KEY, SABaseView


def test_sa_session(mocked_request, orm_session):
    mocked_request[SA_DEFAULT_KEY] = orm_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is orm_session
