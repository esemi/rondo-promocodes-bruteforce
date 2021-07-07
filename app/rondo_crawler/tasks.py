"""Main features of the application."""

import logging
from collections import Counter
from typing import Optional

import trio
from asks import Session, errors

from app import settings
from app.codes import PromoCode, Status, gen_next_code
from app.rondo_crawler.parser import ResponseParser
from app.storage import save_code, update_code_status


async def lookup_codes(codes_limit: int, counter: Counter, session: Session) -> Counter:
    """Lookup potentially valid promo codes."""
    async with trio.open_nursery() as nursery:
        code_gen = gen_next_code(codes_limit, settings.CODE_PREFIX)
        while True:
            try:
                code = next(code_gen)
            except (RuntimeError, StopIteration):
                break

            await update_code_status(code)
            logging.debug('process code %r', code)
            if code.status is not None:
                logging.debug('skip code %s because its already located', code.code)
                counter['skip'] += 1
                continue

            nursery.start_soon(_locate_code_request, counter, code, session)
    return counter


async def check_code_task(counter: Counter, code: PromoCode, session: Session) -> Status:
    """Make check promo-code request."""
    # todo unittest
    logging.debug('task start')

    # todo handle exceptions
    response = await session.post(
        follow_redirects=False,
        timeout=settings.CONNECTION_TIMEOUT,
        cookies=settings.CONNECTION_AUTH,
        persist_cookies=True,
        headers={
            'authority': 'www.rondo.cz',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'accept': '*/*',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': settings.USER_AGENT,
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

    response_code = ResponseParser(response.text).response_status
    counter[response_code] += 1
    if response_code == Status.VALID:
        logging.info('valid code found %s', code.code)

    await save_code(code)

    return response_code


async def _locate_code_request(counter: Counter, code: PromoCode, session: Session) -> Optional[Status]:
    """Make check promo-code request."""
    logging.debug('task start %r', code)

    request_params = {
        'path': '/vyhra/%s' % code.code,
        'timeout': settings.CONNECTION_TIMEOUT,
        'follow_redirects': False,
        'headers': {
            'authority': 'www.rondo.cz',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': settings.USER_AGENT,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # noqa: E501
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        },
    }
    try:
        response = await session.get(**request_params)
    except errors.RequestTimeout as exc:
        logging.warning('task response error %r', exc)
        counter['timeout'] += 1
        return None

    logging.debug('task response %s %s', response, response.text)

    response_status = ResponseParser(response.text).response_status

    counter[response_status] += 1
    if response_status == Status.FOUND:
        logging.info('potentially valid code found %s', code.code)

    code.status = response_status
    logging.info('parsed code %r', code)

    await save_code(code)

    return response_status
