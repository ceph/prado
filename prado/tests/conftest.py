import os
import uuid
from copy import deepcopy
from pecan.testing import load_test_app

from pecan import configuration

import pytest

from prado.tests import util


def config_file():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'config.py')


@pytest.fixture
def b_(request):
    """
    Useful for assertions as everything in the body is now bytes
    """
    def func(s):
        return s.encode("utf-8")
    return func


@pytest.fixture(scope='function')
def app(request):
    _config = configuration.conf_from_file(config_file()).to_dict()
    config = deepcopy(_config)
    configuration.set_config(config, overwrite=True)

    # Set up a fake app
    app = TestApp(load_test_app(config))
    return app


class TestApp(object):
    """
    A controller test starts a database transaction and creates a fake
    WSGI app.
    """

    __headers__ = {}

    def __init__(self, app):
        self.app = app
        self.uuid = uuid.uuid1()

    def _do_request(self, url, method='GET', **kwargs):
        methods = {
            'GET': self.app.get,
            'POST': self.app.post,
            'POSTJ': self.app.post_json,
            'PUT': self.app.put,
            'DELETE': self.app.delete
        }
        kwargs.setdefault('headers', {}).update(self.__headers__)
        return methods.get(method, self.app.get)(str(url), **kwargs)

    def post_json(self, url, **kwargs):
        """
        @param (string) url - The URL to emulate a POST request to
        @returns (paste.fixture.TestResponse)
        """
        # support automatic, correct authentication if not specified otherwise
        if not kwargs.get('headers'):
            kwargs['headers'] = {'Authorization': util.make_credentials()}
        return self._do_request(url, 'POSTJ', **kwargs)

    def post(self, url, **kwargs):
        """
        @param (string) url - The URL to emulate a POST request to
        @returns (paste.fixture.TestResponse)
        """
        # support automatic, correct authentication if not specified otherwise
        if not kwargs.get('headers'):
            kwargs['headers'] = {'Authorization': util.make_credentials()}
        return self._do_request(url, 'POST', **kwargs)

    def get(self, url, **kwargs):
        """
        @param (string) url - The URL to emulate a GET request to
        @returns (paste.fixture.TestResponse)
        """
        # support automatic, correct authentication if not specified otherwise
        if not kwargs.get('headers'):
            kwargs['headers'] = {'Authorization': util.make_credentials()}
        return self._do_request(url, 'GET', **kwargs)

    def put(self, url, **kwargs):
        """
        @param (string) url - The URL to emulate a PUT request to
        @returns (paste.fixture.TestResponse)
        """
        # support automatic, correct authentication if not specified otherwise
        if not kwargs.get('headers'):
            kwargs['headers'] = {'Authorization': util.make_credentials()}
        return self._do_request(url, 'PUT', **kwargs)

    def delete(self, url, **kwargs):
        """
        @param (string) url - The URL to emulate a DELETE request to
        @returns (paste.fixture.TestResponse)
        """
        # support automatic, correct authentication if not specified otherwise
        if not kwargs.get('headers'):
            kwargs['headers'] = {'Authorization': util.make_credentials()}
        return self._do_request(url, 'DELETE', **kwargs)
