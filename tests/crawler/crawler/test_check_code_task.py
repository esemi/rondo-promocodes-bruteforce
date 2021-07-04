from collections import Counter

import pytest as pytest

from crawler.codes import PromoCode, Status
from crawler.crawler import check_code_task, prepare_session


@pytest.mark.parametrize(
    'code, expected',
    [
        ('ZRC0JFZ', Status.ALREADY_USED),
        ('0000000', Status.NOT_FOUND),
    ],
)
async def test_smoke(code: str, expected: Status):
    counter = Counter()

    res = await check_code_task(
        counter,
        PromoCode(code=code, last_status=Status.NOT_FOUND),
        await prepare_session(1),
    )

    assert res == expected
