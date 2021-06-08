from aiohttp_sqlalchemy import SABaseView


def test_sa_session(mocked_request, sa_session):
    mocked_request['sa_main'] = sa_session
    view = SABaseView(mocked_request)
    assert view.sa_session() is sa_session
