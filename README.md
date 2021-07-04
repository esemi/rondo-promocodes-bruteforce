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
```

### run tests
```bash
$ poetry run mypy --ignore-missing-imports crawler/
$ poetry run flake8 crawler
$ poetry run pytest -ra -v --cov=crawler  tests
```

### run crawling
```bash
$ poetry run TODO
```


## TODO
- MVP
- unittests  
- linters  
- CI  
- parse cli args
- readme runner
- deploy to pypi & badges
