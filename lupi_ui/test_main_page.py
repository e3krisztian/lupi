from http import HTTPStatus

import lupi_game_client
import pytest


def test_main_page(client):
    assert client.get('/').status_code == HTTPStatus.OK


def assert_has_active_round(game_api):
    game_api.get_current_round_id()


def assert_has_no_active_round(game_api):
    with pytest.raises(lupi_game_client.ApiException):
        game_api.get_current_round_id()


class Test_start_new_round:
    def test_no_active_round(self, client, game_api, no_active_round, url_for):
        rv = client.post(url_for('lupi_ui.start_round'), follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_active_round(game_api)

    def test_active_round(self, client, game_api, active_round_id, url_for):
        rv = client.post(url_for('lupi_ui.start_round'), follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert active_round_id == game_api.get_current_round_id()


class Test_close_round:
    def test_no_active_round(self, client, game_api, no_active_round, url_for):
        rv = client.post(url_for('lupi_ui.close_round'), follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_no_active_round(game_api)

    def test_active_round(self, client, game_api, active_round_id, url_for):
        assert active_round_id == game_api.get_current_round_id()

        rv = client.post(url_for('lupi_ui.close_round'), follow_redirects=False)
        assert rv.status_code == HTTPStatus.SEE_OTHER
        rv = client.get(rv.headers['Location'])
        assert rv.status_code == HTTPStatus.OK

        assert_has_no_active_round(game_api)

        game_api.set_round_completed(active_round_id, body=True)

        with pytest.raises(lupi_game_client.ApiException):
            game_api.get_current_round_id()
