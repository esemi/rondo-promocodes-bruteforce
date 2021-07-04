import random
from collections import Counter

from app.crawler import main


async def test_smoke():
    random.seed(None)
    res: Counter = await main(10)

    assert sum(res.values()) == 10
