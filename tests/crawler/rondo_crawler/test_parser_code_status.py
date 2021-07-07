import pytest as pytest

from app.rondo_crawler.parser import ResponseParser

from app.codes import Status


def test_valid_json():
    pass


def test_not_found_json():
    test_response = """ucherForm: "\n\t\t<form action=\"/uzivatel/credit\" 
    method=\"post\" id=\"frm-voucherForm\" class=\"ajax\">\n\t\t<div class=\"row form-group  form-error\">\n\t\t\t
    <div class=\"col-sm-12\">\n\n\t\t\t\t<label for=\"frm-voucherForm-voucherCode\">
    Zadejte dobíjecí kód:</label>\n\t\t\t\t<input type=\"text\" name=\"voucherCode\" id=\"frm-voucherForm-voucherCode\" 
    value=\"ZRC0JFS\" class=\"form-control\">\n\t\t\t\t<p class=\"form-error-text\">Voucher s tímto kódem neexistuje</p>
    \n\t\t\t</div>\n\t\t</div>\n\t\t<div class=\"row form-group margin-bottom-40\">\n\t\t\t<div class=\"col-md-12 
    text-right\">\n\t\t\t\t<input type=\"submit\" name=\"send\" value=\"Dobít\" class=\"btn btn-success\">\n\t\t\t</div>
    \n\t\t</div>\n\t\t<input type=\"hidden\" name=\"_do\" value=\"voucherForm-submit\"><!--[if IE]>
    <input type=IEbug disabled style=\"display:none\"><![endif]-->\n</form>\n\n"""""

    r = ResponseParser(test_response).response_status

    assert r == Status.NOT_FOUND


@pytest.mark.parametrize('source', [
    '<p class="form-error-text">Voucher s tímto kódem byl již použitý.</p>',
    'Zadejte svůj výherní kód</p><p class="error">Litujeme, ale tento kód již expiroval.</p>',
    'Zadejte svůj výherní kód</p><p class="error">Litujeme, ale tento kód byl již využit.</p>',
],)
def test_used(source: str):
    r = ResponseParser(source).response_status
    assert r == Status.ALREADY_USED


def test_found_potentional_valid():
    test_response = """<p class="h2">Zadejte svůj výherní kód z losu.</p>
    <p class="error">Informace o výhře se dozvíte po <a href="/prihlasit/se?backRedir=1">přihlášení</a>.</p>"""

    r = ResponseParser(test_response).response_status

    assert r == Status.FOUND


def test_not_found_html():
    test_response = """Zadejte svůj výherní kód</p>
    <p class="error">Litujeme, ale tento dobíjecí kód neexistuje</p>\""""

    r = ResponseParser(test_response).response_status

    assert r == Status.NOT_FOUND


def test_valid_code():
    test_response = """<p class="h2">Váš los je aktivní!</p>
    <p class="h3">Soutěžte s partnerem Království hraček Bambule a získejte další skvělé bonusy!</p>"""

    r = ResponseParser(test_response).response_status

    assert r == Status.VALID
