from pecan import expose, response, redirect, conf, abort
from webob.static import FileIter


class BuildController(object):

    @expose(content_type='application/octet-stream', generic=True)
    def index(self, **kw):
        # TODO: grab the variables from `kw` and pass them to the templating
        # engine to generate the right playbook variables
        response.headers['Content-Disposition'] = 'attachment; filename=playbook.tar.gz'
        response.headers['X-Accel-Redirect'] = 'playbook.tar.gz'
        # FIXME: this needs to be programatic because we might get a lot of
        # these given the different variables. Maybe a temporary location?
        f = open(conf.playbook, 'rb')
        response.app_iter = FileIter(f)

