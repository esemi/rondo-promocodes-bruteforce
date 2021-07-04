"""Operations with promo-code objects."""
import itertools
import random
import string
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterator

CODE_LEN = 7


class Status(IntEnum):
    NOT_FOUND = auto()
    VALID = auto()
    ALREADY_USED = auto()


@dataclass
class PromoCode:  # noqa: WPS306
    code: str
    last_status: Status


def alphabet_permutations(repeat: int) -> itertools.product:
    alphabet = list(string.digits + string.ascii_uppercase)
    random.shuffle(alphabet)
    return itertools.product(''.join(alphabet), repeat=repeat)


def gen_next_code(limit: int) -> Iterator[PromoCode]:
    permutations = alphabet_permutations(CODE_LEN)
    for _ in range(limit):
        code = ''.join(next(permutations))
        status = Status.NOT_FOUND
        yield PromoCode(code, status)
