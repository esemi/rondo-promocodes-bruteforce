# shiny-octo-spork

[![wemake-python-styleguide](https://github.com/esemi/shiny-octo-spork/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/shiny-octo-spork/actions/workflows/linters.yml)
[![pytest](https://github.com/esemi/shiny-octo-spork/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/esemi/shiny-octo-spork/actions/workflows/unittests.yml)
---

## Project local running

### install
```bash
$ git clone PATH

$ cd shiny-octo-spork
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install poetry
$ poetry install
cat > .env << EOF
SESSION_ID="U_PHPSESSID_COOKIE_VALUE_HERE"
EOF

```

### run tests
```bash
$ poetry run mypy --ignore-missing-imports app/
$ poetry run flake8 app
$ poetry run pytest -ra -v --cov=app  tests
```

### run crawling
```bash
$ poetry run TODO
```


## TODO
- ~~unittests~~  
- ~~linters~~  
- ~~CI~~  
- ~~MVP~~
- parse cli args
- readme runner
- deploy to pypi & badges
