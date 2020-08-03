import random
import string
from flask import Flask
from handlers.routes import configure_routes


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
        "body_length": "WRONG_DATA_TYPE",
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

    response_init = client.post(url, json=mock_request_data)
    response = client.post(url, json=mock_request_data)
    assert response.status_code == 400


def test_bird_route_get_basic():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response = client.get(url)
    assert response.status_code == 200
    assert len(response.get_data()) > 0


def test_bird_route_get_sorted():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response = client.get(url, query_string={'attribute': 'name', 'order': 'asc'})
    assert response.status_code == 200
    attr_list = [item['name'] for item in response.get_json()]
    assert attr_list == sorted(attr_list)


def test_bird_route_get_limit():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response = client.get(url, query_string={'limit': 2})
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_bird_route_get_offset():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response_full = client.get(url)
    data1 = response_full.get_json()
    res1 = data1[5]
    response = client.get(url, query_string={'offset': 5})
    data2 = response.get_json()
    res2 = data2[0]
    assert response.status_code == 200
    assert res1 == res2


def test_bird_route_get_empty_params():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response = client.get(url, query_string={'limit': None})
    assert response.status_code == 200
    assert len(response.get_data()) > 0


def test_bird_route_get_wrong_data_type():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/birds'

    response = client.get(url, query_string={'limit': "Hello"})
    assert response.status_code == 500
