"""Crawling ."""

import logging
import time
from collections import Counter

import asks
import asyncclick as click

from app.settings import CONNECTIONS_LIMIT
from app.rondo_crawler.tasks import lookup_codes


async def prepare_session(conn_limit: int) -> asks.Session:
    return asks.Session(
        'https://www.rondo.cz',
        connections=conn_limit,
    )


async def main(limit: int) -> Counter:
    logging.info('app.main started')
    start_time = time.time()

    counter: Counter = Counter()

    session = await prepare_session(CONNECTIONS_LIMIT)

    counter = await lookup_codes(limit, counter, session)
    logging.info('app.main lookup codes %s', counter)

    end_time = time.time() - start_time
    logging.info(
        'app.main ended %s; total_sec=%.2f; tasks_per_sec=%.2f',
        counter,
        end_time,
        sum(counter.values()) / end_time,
    )

    return counter


@click.command()
@click.option('--limit', required=True, default=3, type=int, help='Crawler tasks limit')
@click.option('--verbose', type=bool, default=False, help='Enables verbose mode')
async def runner(limit: int, verbose: bool = False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    await main(limit)
