from pecan import expose
from prado.controllers.setup import SetupController
from prado.controllers.build import BuildsController


class RootController(object):

    @expose('json')
    def index(self):
        return dict()

    setup = SetupController()
    build = BuildsController()
