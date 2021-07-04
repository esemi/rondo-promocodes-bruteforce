import random

import pytest as pytest

from app import codes


@pytest.fixture
def fixture_promo_code() -> codes.PromoCode:
    yield codes.PromoCode('unittest', random.choice(list(codes.Status)))
