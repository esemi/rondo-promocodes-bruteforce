import pytest as pytest

from app.codes import gen_next_code, PromoCode


def test_happy_path():
    res = next(gen_next_code(1))

    assert isinstance(res, PromoCode)
    assert len(res.code) == 7
    assert res.status is None


@pytest.mark.parametrize(
    'limit, expected',
    [(0, 0), (123, 123), (-10, 0)],
)
def test_limit(limit: int, expected: int):
    res = list(gen_next_code(limit))

    assert len(res) == expected


def test_prefix():
    res = next(gen_next_code(1, 'ZRC0'))

    assert isinstance(res, PromoCode)
    assert len(res.code) == 7
    assert res.code.startswith('ZRC0')


def test_stop_iteration():
    gen = gen_next_code(10, '1234567')
    with pytest.raises(RuntimeError):
        for _ in range(11):
            next(gen)
