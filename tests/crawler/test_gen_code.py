from crawler.codes import gen_next_code, Status, PromoCode


def test_happy_path():
    res = gen_next_code()

    assert isinstance(res, PromoCode)
    assert res.last_status is Status.NOT_FOUND
    assert len(res.code) == 7
