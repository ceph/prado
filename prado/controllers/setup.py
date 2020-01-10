from pecan import expose, response, redirect, conf, abort
from pecan.secure import secure
from webob.static import FileIter
from prado.util import make_setup_script
from prado.auth import basic_auth


class SetupScriptController(object):

    def __init__(self, name):
        self.name = name

    @secure(basic_auth)
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

    @expose('json')
    def index(self):
        build_map = conf.build_map.to_dict()
        return dict(
            playbooks=[i for i in build_map.keys()]
        )

    @secure(basic_auth)
    @expose(content_type='application/octet-stream', generic=True)
    def ansible(self):
        """
        Servers the pre-made ansible source to avoid installation of packages
        """
        try:
            conf.setup_ansible
        except (AttributeError, KeyError):
            abort(404, 'setup_ansible value is not configured')
        response.headers['Content-Disposition'] = 'attachment; filename=ansible.tar.gz'
        f = open(conf.setup_ansible, 'rb')
        response.app_iter = FileIter(f)

    @expose()
    def _lookup(self, name, *remainder):
        return SetupScriptController(name), remainder
