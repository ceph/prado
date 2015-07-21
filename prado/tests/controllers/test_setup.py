

class TestSetupController(object):

    def test_configure_playbook(self, app):
        result = app.get('/setup/').json
        assert result == {'playbooks': ['slave']}

    def test_get_ansible_tar(self, app):
        result = app.get('/setup/ansible/', expect_errors=True)
        assert result.status_int == 204

    def test_get_ansible_tar_not_configured(self, app):
        from pecan.configuration import set_config
        set_config({}, overwrite=True)
        result = app.get('/setup/ansible/', expect_errors=True)
        assert result.status_int == 404

    def test_unconfigured_playbook(self, app):
        result = app.get('/setup/unconfigured/', expect_errors=True)
        assert result.status_int == 404

    def test_configured_playbook(self, app):
        result = app.get('/setup/slave/')
        assert result.status_int == 200
