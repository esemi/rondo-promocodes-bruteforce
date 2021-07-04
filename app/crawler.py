"""Crawling functionality."""

import logging
from collections import Counter

import asks
import trio

from app.settings import CONNECTIONS_LIMIT
from app.tasks import lookup_codes


async def prepare_session(conn_limit: int) -> asks.Session:
    return asks.Session(
        'https://www.rondo.cz',
        connections=conn_limit,
    )


async def main(codes_limit: int) -> Counter:
    logging.info('app.main started')
    counter: Counter = Counter()
    session = await prepare_session(CONNECTIONS_LIMIT)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(lookup_codes, codes_limit, counter, session)

    logging.info('app.main lookup codes %s', counter)

    # todo impl parse internal codes
    logging.info('app.main ended %s', counter)
    return counter


if __name__ == '__main__':
    # todo setup logging
    # todo parse cli
    logging.basicConfig(level=logging.INFO)
    limit = 1
    trio.run(main, limit)
