from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterator

CODE_LEN = 7


class Status(IntEnum):
    NOT_FOUND = auto()
    VALID = auto()
    ALREADY_USED = auto()


@dataclass
class PromoCode:
    code: str
    last_status: Status


def generate_code() -> str:
    return 'todo'.zfill(CODE_LEN)


def gen_next_code(limit: int) -> Iterator[PromoCode]:
    for i in range(limit):
        code = generate_code()
        status = Status.NOT_FOUND
        yield PromoCode(code, status)
