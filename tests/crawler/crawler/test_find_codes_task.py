from collections import Counter

import pytest as pytest

from app.codes import PromoCode, Status
from app.crawler import prepare_session
from app.tasks import _locate_code_task


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
    code = PromoCode(code, Status.NOT_FOUND)
    assert code.status == Status.NOT_FOUND

    res = await _locate_code_task(counter, code, await prepare_session(1))

    assert res == expected
    assert code.status == expected
