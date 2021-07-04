from crawler.crawler import main


async def test_smoke():
    res = await main(10)

    assert res == []
