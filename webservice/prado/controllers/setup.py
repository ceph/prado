from pecan import expose, response, redirect, conf, abort
from webob.static import FileIter
from prado.util import make_setup_script


class SetupScriptController(object):

    def __init__(self, name):
        self.name = name

    @expose(content_type='application/octet-stream')
    def index(self, **kw):
        try:
            conf.build_map[self.name]
        except (AttributeError, KeyError):
            abort(404)

        script = make_setup_script(self.name, **kw)

        response.headers['Content-Disposition'] = 'attachment; filename=setup.sh'
        response.app_iter = FileIter(script)


class SetupController(object):

    @expose(content_type='application/octet-stream', generic=True)
    def index(self):
        response.headers['Content-Disposition'] = 'attachment; filename=setup.sh'
        f = open(conf.setup_script, 'rb')
        response.app_iter = FileIter(f)

    @expose(content_type='application/octet-stream', generic=True)
    def ansible(self):
        """
        Servers the pre-made ansible source to avoid installation of packages
        """
        response.headers['Content-Disposition'] = 'attachment; filename=ansible.tar.gz'
        f = open(conf.setup_ansible, 'rb')
        response.app_iter = FileIter(f)

    @expose()
    def _lookup(self, name, *remainder):
        return SetupScriptController(name), remainder
