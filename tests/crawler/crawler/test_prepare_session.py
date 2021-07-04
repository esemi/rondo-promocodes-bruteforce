import asks

from app.crawler import prepare_session


async def test_smoke():
    res = await prepare_session(10)

    assert isinstance(res, asks.Session)
    assert res.sema.value == 10

