from collections import Counter

from crawler.codes import Status
from crawler.crawler import main


async def test_smoke():
    res: Counter = await main(10)

    assert res.get(Status.NOT_FOUND) == 10
    assert sum(res.values()) == 10
