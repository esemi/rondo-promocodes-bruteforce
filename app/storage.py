"""Interface to storage of codes."""
from typing import Optional

import redio

from app import codes, settings

redis_pool = redio.Redis(settings.REDIS_DST)


def index_promo_code(code: str) -> str:
    return 'rondo_crawler:code:%s' % code


async def save_code(code: codes.PromoCode):
    index = index_promo_code(code.code)
    await redis_pool().set(index, code.status.value)


async def fetch_code_status(code: codes.PromoCode) -> Optional[str]:
    index = index_promo_code(code.code)
    index_value = await redis_pool().get(index)
    return None if not index_value else index_value.decode()


async def update_code_status(code: codes.PromoCode):
    """Update PromoCode.status inplace if exist in storage."""
    status = await fetch_code_status(code)
    if status:
        code.status = codes.Status(status)
