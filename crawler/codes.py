from dataclasses import dataclass
from enum import IntEnum, auto

CODE_LEN = 7


class Status(IntEnum):
    NOT_FOUND = auto()
    VALID = auto()
    ALREADY_USED = auto()


@dataclass
class PromoCode:
    code: str
    last_status: Status


def gen_next_code() -> PromoCode:
    code = 'todo'.zfill(CODE_LEN)
    status = Status.NOT_FOUND
    return PromoCode(code, status)
