"""Promo-code validation response parser."""

from app.codes import Status


class ResponseParser(object):
    _response_content: str

    def __init__(self, response: str):
        self._response_content = response

    @property
    def is_not_found_code(self) -> bool:
        patterns = {'tímto kódem neexistuje', 'tento dobíjecí kód neexistuje'}
        return any(map(lambda substr: substr in self._response_content, patterns))

    @property
    def is_used_code(self) -> bool:
        patterns = {'tímto kódem byl již použitý', 'ale tento kód byl již využit', 'ale tento kód již expiroval'}
        return any(map(lambda substr: substr in self._response_content, patterns))

    @property
    def is_found_code(self) -> bool:
        return 'Informace o výhře se dozvíte po ' in self._response_content

    @property
    def is_valid_code(self) -> bool:
        return 'Váš los je aktivní' in self._response_content

    @property
    def response_status(self) -> Status:
        if self.is_not_found_code:
            return Status.NOT_FOUND

        if self.is_used_code:
            return Status.ALREADY_USED

        if self.is_found_code:
            return Status.FOUND

        if self.is_valid_code:
            return Status.VALID

        raise NotImplementedError('Invalid response %s' % self._response_content)
