from collections import Counter

import pytest as pytest

from crawler.codes import PromoCode, Status
from crawler.crawler import locate_code_task, prepare_session


@pytest.mark.parametrize(
    'code, expected',
    [
        ('ZRC0JFZ', Status.FOUND),
        ('0000000', Status.NOT_FOUND),
        ('1111111', Status.NOT_FOUND),
    ],
)
async def test_locate_code_task_smoke(code: str, expected: Status):
    counter = Counter()
    code = PromoCode(code=code, last_status=Status.NOT_FOUND)

    res = await locate_code_task(counter, code, await prepare_session(1))

    assert res == expected
    assert code.current_status == expected
    assert code.last_status == Status.NOT_FOUND
