"""Interface to storage of codes."""

from crawler import codes


def index_promo_code(code: str) -> str:
    return 'rondo_crawler:code:%s' % code


async def save_code(code: codes.PromoCode):
    # todo impl + test
    pass


async def update_code_status(code: codes.PromoCode):
    """Update PromoCode.status inplace if exist in storage."""
    # todo impl + test
    status = None
    if status:
        code.status = codes.Status(status)
