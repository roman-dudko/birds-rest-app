# REST API appilcation for interaction with 'birds' database

> Uses Python Flask, SQL Alchemy and Marshmallow

## Start Application Using Pipenv

``` bash
# Prepare test DB
docker pull ostadnick/birds-db
docker run -p 5432:5432 -d ostadnick/birds-db

# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Run Server (http://localhst:5000)
$ python app.py
```

## Endpoints

* GET     /version
* GET     /birds (suported params: attribute, order, offset, limit)
* POST    /birds

## Unit tests
``` bash
# Run tests for all endpoints
$ pytest
```
