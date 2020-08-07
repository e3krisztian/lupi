from http import HTTPStatus
from lupi_ui.conftest import active_round_id


class Test_view:
    def test_happy_path_active(self, webui, client, active_round_id):
        url = webui.url_for("lupi_ui.round_details", round_id=active_round_id)
        assert client.get(url).status_code == HTTPStatus.OK

    def test_happy_path_completed_no_winner(self, webui, client, server, active_round_id):
        server.game.set_round_completed(active_round_id, body=True)
        url = webui.url_for("lupi_ui.round_details", round_id=active_round_id)
        assert client.get(url).status_code == HTTPStatus.OK

    # TODO: test_happy_path_completed_has_winner
    # TODO: test_invalid_round_id
