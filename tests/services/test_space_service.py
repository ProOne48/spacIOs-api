import pytest
import flask


@pytest.mark.usefixtures('client_class')
class TestSpaceService(object):
    def test_list(self, insert_space_owner, insert_space, cookie_jwt_auth_header):
        url = flask.url_for('Space.get_spaces')
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.get(url)

        assert res.json.get('total') == 1

    def test_get_space_by_id(self, insert_space_owner, insert_space, cookie_jwt_auth_header):
        url = flask.url_for('Space.get_space_by_id', space_id=insert_space.id)
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.get(url)

        assert res.json.get('id') == insert_space.id
        assert res.json.get('name') == insert_space.name

    def test_delete_space(self, insert_space_owner, insert_space, cookie_jwt_auth_header):
        url = flask.url_for('Space.delete_space', space_id=insert_space.id)
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.delete(url)

        assert res.status_code == 204
