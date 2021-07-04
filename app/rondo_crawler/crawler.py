"""Crawling ."""

import logging
from collections import Counter

import asks
import asyncclick as click
import trio

from app.settings import CONNECTIONS_LIMIT
from app.tasks import lookup_codes


async def prepare_session(conn_limit: int) -> asks.Session:
    return asks.Session(
        'https://www.rondo.cz',
        connections=conn_limit,
    )


@click.command()
@click.option("--limit", required=True, default=3, type=int, help='Crawler tasks limit')
@click.option("--verbose", type=bool, default=False, help="Enables verbose mode")
async def main(limit: int, verbose: bool = False) -> Counter:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    logging.info('app.main started')
    counter: Counter = Counter()
    session = await prepare_session(CONNECTIONS_LIMIT)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(lookup_codes, limit, counter, session)

    logging.info('app.main lookup codes %s', counter)

    # todo impl parse internal codes
    logging.info('app.main ended %s', counter)
    return counter
