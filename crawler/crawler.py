"""Crawling functionality."""

import logging
from collections import Counter
from types import MappingProxyType

import asks
import trio

from crawler import codes, settings

CONNECTIONS_LIMIT = 10
CONNECTION_TIMEOUT = 5
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
CONNECTION_AUTH = MappingProxyType({
    'rndu': 'MzQ3NDk2OA%3D%3D%3AnGNWiA',
    'roperm': 'MzQ3NDk2OHwqKnwxYmMyNTIzNTcxZWNkYmY0NWY2ZjJjMjdlOWQ0OGJiMQ%3D%3D%3Ap9ubsQ',
    'PHPSESSID': settings.SESSION_ID,
    'lastLogin': 'MTYyNTM0MzMxMQ%3D%3D%3AjvYAig',
})


async def prepare_session(conn_limit: int) -> asks.Session:
    return asks.Session(
        'https://www.rondo.cz',
        connections=conn_limit,
    )


def determine_code_status(response: str) -> codes.Status:
    if 'tímto kódem neexistuje' in response:
        return codes.Status.NOT_FOUND

    elif 'tento dobíjecí kód neexistuje' in response:
        return codes.Status.NOT_FOUND

    elif 'tímto kódem byl již použitý' in response:
        return codes.Status.ALREADY_USED

    elif 'Informace o výhře se dozvíte po ' in response:
        return codes.Status.FOUND

    # todo impl
    raise NotImplementedError('Invalid response %s' % response)


async def locate_code_task(counter: Counter, code: codes.PromoCode, session: asks.Session) -> codes.Status:
    """Make check promo-code request."""
    logging.debug('task start %r', code)
    # todo handle exceptions

    response = await session.get(
        path='/vyhra/%s' % code.code,
        timeout=CONNECTION_TIMEOUT,
        follow_redirects=False,
        headers={
            'authority': 'www.rondo.cz',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': USER_AGENT,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # noqa: E501
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        },
    )
    logging.debug('task response %s %s', response, response.text)

    response_status = determine_code_status(response.text)
    counter[response_status] += 1
    if response_status is codes.Status.FOUND:
        logging.info('potentially valid code found %s', code.code)

    code.current_status = response_status
    return response_status


async def check_code_task(counter: Counter, code: codes.PromoCode, session: asks.Session) -> codes.Status:
    """Make check promo-code request."""
    logging.debug('task start')
    # todo handle exceptions

    response = await session.post(
        follow_redirects=False,
        timeout=CONNECTION_TIMEOUT,
        cookies=CONNECTION_AUTH,
        persist_cookies=True,
        headers={
            'authority': 'www.rondo.cz',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': '*/*',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': USER_AGENT,
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.rondo.cz/uzivatel/credit',
        },
        data={
            'voucherCode': code.code,
            '_do': 'voucherForm-submit',
            'send': 'Dob%C3%ADt',
        },
    )
    logging.debug('task response %s %s', response, response.text)

    response_code = determine_code_status(response.text)
    counter[response_code] += 1
    if response_code is codes.Status.VALID:
        logging.info('valid code found %s', code.code)

    # todo save result to redis

    return response_code


async def main(codes_limit: int) -> Counter:
    logging.info('crawler.main started')
    counter: Counter = Counter()
    session = await prepare_session(CONNECTIONS_LIMIT)

    async with trio.open_nursery() as nursery:
        for code in codes.gen_next_code(codes_limit):
            nursery.start_soon(locate_code_task, counter, code, session)
    logging.info('crawler.main ended %s', counter)
    return counter


if __name__ == '__main__':
    # todo setup logging
    # todo parse cli
    logging.basicConfig(level=logging.DEBUG)
    limit = 1
    trio.run(main, limit)
