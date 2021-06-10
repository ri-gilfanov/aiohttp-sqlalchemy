from aiohttp_sqlalchemy import DEFAULT_KEY, sa_session


def test_sa_session(mocked_request, orm_session):
    mocked_request[DEFAULT_KEY] = orm_session
    assert sa_session(mocked_request) is orm_session
