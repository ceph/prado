from pecan import expose, redirect
from prado.controllers.setup import SetupController
from prado.controllers.build import BuildController


class RootController(object):

    @expose('json')
    def index(self):
        return dict()

    setup = SetupController()
    build = BuildController()
