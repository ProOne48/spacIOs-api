import flask
import pytest

API_BLUEPRINT = 'SpaceOwner'


@pytest.mark.usefixtures('client_class')
class TestSpaceOwnerService(object):
    def test_list(self, insert_space_owner, cookie_jwt_auth_header):
        url = flask.url_for(f'{API_BLUEPRINT}.get_space_owners')
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.get(url)

        assert res.json.get('total') == 1

    def test_get_space_owner_by_id(self, insert_space_owner, cookie_jwt_auth_header):
        url = flask.url_for(f'{API_BLUEPRINT}.get_space_owner_by_id', space_owner_id=insert_space_owner.id)
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.get(url)

        assert res.json.get('name') == insert_space_owner.name
        assert res.json.get('email') == insert_space_owner.email

    def test_delete_space_owner(self, insert_space_owner, cookie_jwt_auth_header):
        url = flask.url_for(f'{API_BLUEPRINT}.delete_space_owner', space_owner_id=insert_space_owner.id)
        self.client.set_cookie('localhost', cookie_jwt_auth_header[0], cookie_jwt_auth_header[1])
        res = self.client.delete(url)

        assert res.status_code == 204
