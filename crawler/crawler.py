import logging
from collections import Counter

import trio
import asks

import codes


CONNECTIONS_LIMIT = 10

s = asks.Session('https://www.rondo.cz/uzivatel/credit',
                 connections=CONNECTIONS_LIMIT)


def determine_code_status(response: str) -> codes.Status:
    if 'Voucher s tímto kódem neexistuje' in response:
        return codes.Status.NOT_FOUND
    elif 'Voucher s tímto kódem byl již použitý' in response:
        return codes.Status.ALREADY_USED
    else:
        # todo impl
        raise NotImplementedError('Invalid response %s' % response)


async def check_code_task(counter: Counter, code: codes.PromoCode) -> codes.Status:
    logging.debug('task start')
    # todo handle exceptions
    r = await s.post()
    logging.debug('task response %s %s', r, r.content)

    # todo parse response
    response_code = determine_code_status(r.content)
    counter[response_code] += 1
    if response_code is codes.Status.VALID:
        logging.info('valid code found %s', code.code)

    return codes.Status.NOT_FOUND


async def main(limit: int):
    logging.info('crawler.main started')
    counter = Counter()
    async with trio.open_nursery() as nursery:
        for code in codes.gen_next_code(limit):
            nursery.start_soon(check_code_task, counter, code)
    logging.info('crawler.main ended %s', counter)


if __name__ == '__main__':
    # todo setup logging
    # todo parse cli
    logging.basicConfig(level=logging.DEBUG)
    limit = 1
    trio.run(main, limit)
