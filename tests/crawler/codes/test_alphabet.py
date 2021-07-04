import math
import random
from typing import Iterator

import pytest as pytest

from crawler.codes import alphabet_permutations


@pytest.mark.parametrize(
    'substr_len',
    [1, 2, 3, 4],
)
def test_alphabet_permutations_counter(substr_len: int):
    res = alphabet_permutations(substr_len)

    assert isinstance(res, Iterator)
    assert len(list(res)) == math.pow(36, substr_len)


def test_alphabet_permutations():
    random.seed('unittests123')

    res = list(map(lambda x: ''.join(x), alphabet_permutations(2)))

    assert res[:10] == ['55', '51', '5F', '5N', '5K', '5W', '5Y', '54', '5I', '5X']
