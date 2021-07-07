import pytest as pytest

from app import codes
from app.storage import save_code, fetch_status, update_code_status, fetch_codes


async def test_save_fetch(fixture_promo_code: codes.PromoCode):
    await save_code(fixture_promo_code)

    res = await fetch_status(fixture_promo_code)
    assert res == fixture_promo_code.status.value

    res = await fetch_codes(fixture_promo_code.status)
    assert len(res) > 0
    assert fixture_promo_code.code in res


async def test_save_failure(fixture_promo_code: codes.PromoCode):
    fixture_promo_code.status = None

    with pytest.raises(RuntimeError):
        await save_code(fixture_promo_code)


async def test_fetch_status_not_found():
    res = await fetch_status(codes.PromoCode(code='not found key'))

    assert res is None


async def test_update_code_status(fixture_promo_code: codes.PromoCode):
    await save_code(fixture_promo_code)
    original_status = fixture_promo_code.status
    fixture_promo_code.status = 'changed'

    assert fixture_promo_code.status == 'changed'
    await update_code_status(fixture_promo_code)

    assert fixture_promo_code.status == original_status


async def test_fetch_codes():
    res = await fetch_codes(codes.Status.VALID)

    assert isinstance(res, list)
    assert len(res) >= 0
    for i in res:
        assert isinstance(i, str)
