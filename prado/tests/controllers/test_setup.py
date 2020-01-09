

class TestSetupController(object):

    def test_configure_playbook(self, app):
        result = app.get('/setup/').json
        playbooks = result['playbooks']
        assert playbooks == ['novars', 'slave', 'vars']

    def test_get_ansible_tar(self, app):
        result = app.get('/setup/ansible/', expect_errors=True)
        assert result.status_int == 200

    def test_get_ansible_tar_not_configured(self, app):
        from pecan.configuration import set_config
        set_config({"api_user": "user", "api_key": "key"}, overwrite=True)
        result = app.get('/setup/ansible/', expect_errors=True)
        assert result.status_int == 404

    def test_unconfigured_playbook(self, app):
        result = app.get('/setup/unconfigured/', expect_errors=True)
        assert result.status_int == 404

    def test_configured_playbook(self, app):
        result = app.get('/setup/slave/')
        assert result.status_int == 200

    def test_varargs(self, app):
        result = app.get('/setup/vars/?node_description=Ubuntu Precise Slave x86_64 Build Server&nodename=precise&labels=amd64 precise-pbuild x86_64&token=7479f92lff630c7436318580de6f3e27')
        assert result

    def test_varargs_dunder_dunder(self, app):
        result = app.get('/setup/vars/?node_description=Ubuntu Precise Slave x86_64 Build Server&nodename=precise__some-hash&labels=amd64 precise-pbuild x86_64&token=7479f92lff630c7436318580de6f3e27')
        assert 'precise__some-hash' in result.body
