"""Crawling functionality."""

import logging
from collections import Counter

import asks
import trio

from crawler import codes, settings

CONNECTIONS_LIMIT = 10
CONNECTION_TIMEOUT = 5
RONDO_AUTH = {
    'rndu': 'MzQ3NDk2OA%3D%3D%3AnGNWiA',
    'roperm': 'MzQ3NDk2OHwqKnwxYmMyNTIzNTcxZWNkYmY0NWY2ZjJjMjdlOWQ0OGJiMQ%3D%3D%3Ap9ubsQ',
    'PHPSESSID': settings.SESSION_ID,
    'lastLogin': 'MTYyNTM0MzMxMQ%3D%3D%3AjvYAig',
}


async def prepare_session(conn_limit: int) -> asks.Session:
    session = asks.Session(
        'https://www.rondo.cz/uzivatel/credit',
        connections=conn_limit,
        persist_cookies=True,
    )

    return session


def determine_code_status(response: str) -> codes.Status:
    if 'tímto kódem neexistuje' in response:
        return codes.Status.NOT_FOUND
    elif 'tímto kódem byl již použitý' in response:
        return codes.Status.ALREADY_USED

    # todo impl
    raise NotImplementedError('Invalid response %s' % response)


async def check_code_task(counter: Counter, code: codes.PromoCode, session: asks.Session) -> codes.Status:
    """Make check promo-code request.

    curl 'https://www.rondo.cz/uzivatel/credit' \
      -H 'authority: www.rondo.cz' \
      -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' \
      -H 'accept: */*' \
      -H 'dnt: 1' \
      -H 'x-requested-with: XMLHttpRequest' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36' \
      -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
      -H 'origin: https://www.rondo.cz' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: cors' \
      -H 'sec-fetch-dest: empty' \
      -H 'referer: https://www.rondo.cz/uzivatel/credit' \
      -H 'accept-language: en-US,en;q=0.9,ru;q=0.8' \
      -H 'cookie: rndu=MzQ3NDk2OA%3D%3D%3AnGNWiA; roperm=MzQ3NDk2OHwqKnwxYmMyNTIzNTcxZWNkYmY0NWY2ZjJjMjdlOWQ0OGJiMQ%3D%3D%3Ap9ubsQ; PHPSESSID=jah8vrat6fgbiqf04itl5172u0; lastLogin=MTYyNTM0MzMxMQ%3D%3D%3AjvYAig' \
      --data-raw 'voucherCode=ZRC0JF&_do=voucherForm-submit&send=Dob%C3%ADt' \
      --compressed

    """
    logging.debug('task start')
    # todo handle exceptions

    response = await session.post(
        follow_redirects=False,
        timeout=CONNECTION_TIMEOUT,
        cookies=RONDO_AUTH,
        headers={
            'authority': 'www.rondo.cz',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': '*/*',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
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
        print()

    # todo save result to redis

    return response_code


async def main(codes_limit: int) -> Counter:
    logging.info('crawler.main started')
    counter: Counter = Counter()
    session = await prepare_session(CONNECTIONS_LIMIT)

    async with trio.open_nursery() as nursery:
        for code in codes.gen_next_code(codes_limit):
            nursery.start_soon(check_code_task, counter, code, session)
    logging.info('crawler.main ended %s', counter)
    return counter


if __name__ == '__main__':
    # todo setup logging
    # todo parse cli
    logging.basicConfig(level=logging.DEBUG)
    limit = 1
    trio.run(main, limit)
