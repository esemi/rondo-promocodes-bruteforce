import logging
from collections import Counter

import asks
import trio

from app.codes import gen_next_code, PromoCode, Status
from app.settings import CONNECTION_TIMEOUT, USER_AGENT
from app.storage import update_code_status, save_code


async def lookup_codes(codes_limit: int, counter: Counter, session: asks.Session) -> Counter:
    """Lookup potentially valid promo codes."""
    async with trio.open_nursery() as nursery:
        for code in gen_next_code(codes_limit):
            await update_code_status(code)
            if code.status is not None:
                logging.info('skip code %s because its already located', code.code)
                continue

            nursery.start_soon(_locate_code_task, counter, code, session)
    return counter


#
# async def check_code_task(counter: Counter, code: codes.PromoCode, session: asks.Session) -> codes.Status:
#     """Make check promo-code request."""
#     logging.debug('task start')
#     # todo handle exceptions
#
#     response = await session.post(
#         follow_redirects=False,
#         timeout=CONNECTION_TIMEOUT,
#         cookies=CONNECTION_AUTH,
#         persist_cookies=True,
#         headers={
#             'authority': 'www.rondo.cz',
#             'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
#             'accept': '*/*',
#             'dnt': '1',
#             'x-requested-with': 'XMLHttpRequest',
#             'sec-ch-ua-mobile': '?0',
#             'user-agent': USER_AGENT,
#             'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-dest': 'empty',
#             'referer': 'https://www.rondo.cz/uzivatel/credit',
#         },
#         data={
#             'voucherCode': code.code,
#             '_do': 'voucherForm-submit',
#             'send': 'Dob%C3%ADt',
#         },
#     )
#     logging.debug('task response %s %s', response, response.text)
#
#     response_code = determine_code_status(response.text)
#     counter[response_code] += 1
#     if response_code is codes.Status.VALID:
#         logging.info('valid code found %s', code.code)
#
#     # todo save result to redis
#
#     return response_code


async def _locate_code_task(counter: Counter, code: PromoCode, session: asks.Session) -> Status:
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
    if response_status == Status.FOUND:
        logging.info('potentially valid code found %s', code.code)

    code.status = response_status

    await save_code(code)

    return response_status


def determine_code_status(response: str) -> Status:
    if 'tímto kódem neexistuje' in response:
        return Status.NOT_FOUND

    elif 'tento dobíjecí kód neexistuje' in response:
        return Status.NOT_FOUND

    elif 'tímto kódem byl již použitý' in response:
        return Status.ALREADY_USED

    elif 'Informace o výhře se dozvíte po ' in response:
        return Status.FOUND

    # todo impl
    raise NotImplementedError('Invalid response %s' % response)
