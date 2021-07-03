import pytest as pytest

from crawler.codes import gen_next_code, Status, PromoCode


def test_happy_path():
    res = next(gen_next_code(1))

    assert isinstance(res, PromoCode)
    assert res.last_status is Status.NOT_FOUND
    assert len(res.code) == 7


@pytest.mark.parametrize(
    'limit, expected',
    [(0, 0), (123, 123), (-10, 0)],
)
def test_limit(limit: int, expected: int):
    res = list(gen_next_code(limit))

    assert len(res) == expected
