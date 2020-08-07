from http import HTTPStatus

import lupi_game_client
import pytest


def test_main_page(client):
    assert client.get('/').status_code == HTTPStatus.OK


def assert_has_active_round(server):
    server.game.get_current_round_id()


def assert_has_no_active_round(server):
    with pytest.raises(lupi_game_client.ApiException):
        server.game.get_current_round_id()


class Test_start_new_round:
    def test_no_active_round(self, webui, client, server, no_active_round):
        rv = client.post(
            webui.url_for('lupi_ui.start_round'),
            follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_active_round(server)

    def test_active_round(self, webui, client, server, active_round_id):
        rv = client.post(
            webui.url_for('lupi_ui.start_round'),
            follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert active_round_id == server.game.get_current_round_id()


class Test_close_round:
    def test_no_active_round(self, webui, client, server, no_active_round):
        rv = client.post(
            webui.url_for('lupi_ui.close_round'),
            follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_no_active_round(server)

    def test_active_round(self, webui, client, server, active_round_id):
        assert active_round_id == server.game.get_current_round_id()

        rv = client.post(
            webui.url_for('lupi_ui.close_round'),
            follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_no_active_round(server)

        server.game.set_round_completed(active_round_id, body=True)

        with pytest.raises(lupi_game_client.ApiException):
            server.game.get_current_round_id()


class Test_vote:
    def test_happy_path(self, webui, client, server, active_round_id):
        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='name', number=197),
            follow_redirects=False)

        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK
        assert 'Vote registered' in rv.get_data(as_text=True)

    def test_no_name(self, webui, client, server, no_active_round):
        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='', number=197),
            follow_redirects=False)

        assert rv.status_code == HTTPStatus.OK
        assert '197' in rv.get_data(as_text=True)

    def test_invalid_number(self, webui, client, server, no_active_round):
        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='name', number=-1),
            follow_redirects=False)

        assert rv.status_code == HTTPStatus.OK
        assert '-1' in rv.get_data(as_text=True)
        assert 'Number must be at least 1.' in rv.get_data(as_text=True)

    def test_no_active_round(self, webui, client, server, no_active_round):
        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='a', number=1),
            follow_redirects=False)

        assert rv.status_code == HTTPStatus.OK
        assert 'Can not register vote' in rv.get_data(as_text=True)

    def test_already_voted(self, webui, client, server, active_round_id):
        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='name', number=197),
            follow_redirects=True)
        assert 'Vote registered' in rv.get_data(as_text=True)

        rv = client.post(
            webui.url_for('lupi_ui.vote'),
            data=dict(name='name', number=197),
            follow_redirects=False)

        assert rv.status_code == HTTPStatus.OK
        assert 'Can not register vote' in rv.get_data(as_text=True)
        assert 'already voted' in rv.get_data(as_text=True)
