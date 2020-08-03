from flask import Flask
from handlers.routes import configure_routes
import random
import string


def test_version_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/version'

    response = client.get(url)
    assert response.get_data() == b'Birds Service. Version 0.1'
    assert response.status_code == 200


def test_bird_route_post_success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'
    new_bird = ''.join(random.choice(string.ascii_letters) for i in range(10))

    mock_request_data = {
        "body_length": 1000,
        "color": "red & white",
        "name": new_bird,
        "species": "pigeon",
        "wingspan": 1000
    }

    response = client.post(url, json=mock_request_data)
    assert response.status_code == 200


def test_bird_route_post_wrong_data_type():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    mock_request_data = {
        "body_length": "1000",
        "color": "red & white",
        "name": "test_bird",
        "species": "pigeon",
        "wingspan": 1000
    }

    response = client.post(url, json=mock_request_data)
    assert response.status_code == 400


def test_bird_route_post_inconsistent_data():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    mock_request_data = {
        "body_length": 1000,
        "name": "test_bird",
        "wingspan": 1000
    }

    response = client.post(url, json=mock_request_data)
    assert response.status_code == 400


def test_bird_route_post_duplicate_entity():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'
    new_bird = ''.join(random.choice(string.ascii_letters) for i in range(10))

    mock_request_data = {
        "body_length": 1000,
        "color": "red & white",
        "name": new_bird,
        "species": "pigeon",
        "wingspan": 1000
    }

    response = client.post(url, json=mock_request_data)
    response = client.post(url, json=mock_request_data)
    assert response.status_code == 400


# test_bird_route_get_all
# get sorted asc/desc
# get offset/limit
# combined request

# empty paeams
# incorrect params
