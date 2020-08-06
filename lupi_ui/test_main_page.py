from http import HTTPStatus

def test_main_page(client):
    assert client.get('/').status_code == HTTPStatus.OK
