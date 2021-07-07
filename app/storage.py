"""Interface to storage of codes."""
from typing import List, Optional

import redio

from app import codes, settings

redis_pool = redio.Redis(settings.REDIS_DST)
NAMESPACE = 'rondo_crawler'


def index_promo_code(code: str) -> str:
    return '%s:code:%s' % (NAMESPACE, code)


def index_promo_code_status(status: str) -> str:
    return '%s:status:%s' % (NAMESPACE, status)


async def save_code(code: codes.PromoCode):
    index = index_promo_code(code.code)
    if not code.status:
        raise RuntimeError('Not specified promo code status.')

    if code.status in {codes.Status.VALID, codes.Status.FOUND}:
        status_index = index_promo_code_status(code.status.value)
        await redis_pool().sadd(status_index, code.code)

    await redis_pool().set(index, code.status.value)


async def fetch_status(code: codes.PromoCode) -> Optional[str]:
    index = index_promo_code(code.code)
    index_value = await redis_pool().get(index)

    return index_value if index_value is None else index_value.decode()


async def fetch_codes(status: codes.Status) -> List[str]:
    status_index = index_promo_code_status(status.value)
    codes_by_status = await redis_pool().smembers(status_index)
    return list(map(lambda member: member.decode(), codes_by_status))


async def update_code_status(code: codes.PromoCode):
    """Update PromoCode.status inplace if exist in storage."""
    status = await fetch_status(code)
    if status:
        code.status = codes.Status(status)
