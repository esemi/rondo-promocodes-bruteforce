"""Operations with promo-code objects."""
import itertools
import random
import string
from dataclasses import dataclass
from enum import Enum, unique
from typing import Iterator, Optional

CODE_LEN = 7


@unique
class Status(str, Enum):
    NOT_FOUND = 'not_found'
    FOUND = 'found'
    VALID = 'valid'
    ALREADY_USED = 'used'


@dataclass
class PromoCode:  # noqa: WPS306
    code: str
    status: Optional[Status] = None


def alphabet_permutations(repeat: int) -> itertools.product:
    alphabet = list(string.digits + string.ascii_uppercase)
    random.shuffle(alphabet)
    return itertools.product(''.join(alphabet), repeat=repeat)


def gen_next_code(limit: int, prefix: str = '') -> Iterator[PromoCode]:
    permutations = alphabet_permutations(CODE_LEN - len(prefix))
    for _ in range(limit):
        code = ''.join(next(permutations))
        yield PromoCode(code='%s%s' % (prefix, code))
