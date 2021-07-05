from app.rondo_crawler import crawler


async def test_main():
    res = await crawler.main(2)
    assert sum(res.values()) == 2
