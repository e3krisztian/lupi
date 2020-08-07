from http import HTTPStatus
from lupi_ui.conftest import active_round_id


class Test_view:
    def test_happy_path_maybe_empty(self, webui, client):
        url = webui.url_for("lupi_ui.rounds_history")
        assert client.get(url).status_code == HTTPStatus.OK

    def test_happy_path_non_empty(self, webui, client, server, active_round_id):
        server.game.set_round_completed(active_round_id, body=True)
        url = webui.url_for("lupi_ui.rounds_history")
        assert client.get(url).status_code == HTTPStatus.OK


class Test_paging:
    # TODO: history paging is untested
    pass
