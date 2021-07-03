from crawler.crawler import determine_code_status

from crawler.codes import Status


def test_valid_code():
    pass


def test_not_found_code():
    test_response = """ucherForm: "\n\t\t<form action=\"/uzivatel/credit\" 
    method=\"post\" id=\"frm-voucherForm\" class=\"ajax\">\n\t\t<div class=\"row form-group  form-error\">\n\t\t\t
    <div class=\"col-sm-12\">\n\n\t\t\t\t<label for=\"frm-voucherForm-voucherCode\">
    Zadejte dobíjecí kód:</label>\n\t\t\t\t<input type=\"text\" name=\"voucherCode\" id=\"frm-voucherForm-voucherCode\" 
    value=\"ZRC0JFS\" class=\"form-control\">\n\t\t\t\t<p class=\"form-error-text\">Voucher s tímto kódem neexistuje</p>
    \n\t\t\t</div>\n\t\t</div>\n\t\t<div class=\"row form-group margin-bottom-40\">\n\t\t\t<div class=\"col-md-12 
    text-right\">\n\t\t\t\t<input type=\"submit\" name=\"send\" value=\"Dobít\" class=\"btn btn-success\">\n\t\t\t</div>
    \n\t\t</div>\n\t\t<input type=\"hidden\" name=\"_do\" value=\"voucherForm-submit\"><!--[if IE]>
    <input type=IEbug disabled style=\"display:none\"><![endif]-->\n</form>\n\n"""""

    r = determine_code_status(test_response)

    assert r == Status.NOT_FOUND


def test_used_code():
    test_response = """\n\t\t<form action=\"/uzivatel/credit\" method=\"post\" id=\"frm-voucherForm\" class=\"ajax\">
    \n\t\t<div class=\"row form-group  form-error\">\n\t\t\t<div class=\"col-sm-12\">\n\n\t\t\t\t
    <label for=\"frm-voucherForm-voucherCode\">Zadejte dobíjecí kód:</label>\n\t\t\t\t<input type=\"text\" 
    name=\"voucherCode\" id=\"frm-voucherForm-voucherCode\" value=\"ZRC0JFZ\" class=\"form-control\">\n\t\t\t\t
    <p class=\"form-error-text\">Voucher s tímto kódem byl již použitý.</p>\n\t\t\t</div>\n\t\t</div>\n\t\t
    <div class=\"row form-group margin-bottom-40\">\n\t\t\t<div class=\"col-md-12 text-right\">\n\t\t\t\t
    <input type=\"submit\" name=\"send\" value=\"Dobít\" class=\"btn btn-success\">\n\t\t\t</div>\n\t\t</div>\n\t\t
    <input type=\"hidden\" name=\"_do\" value=\"voucherForm-submit\"><!--[if IE]><input type=IEbug disabled 
    style=\"display:none\"><![endif]-->\n</form>\n\n"""""

    r = determine_code_status(test_response)

    assert r == Status.ALREADY_USED
