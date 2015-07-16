import os
import tempfile
from pecan import expose, response, redirect, conf, abort
from webob.static import FileIter
from prado.util import render, tar_czf


class BuildController(object):

    def __init__(self, name):
        self.name = name

    @expose(content_type='application/octet-stream')
    def index(self, **kw):
        try:
            conf.build_map[self.name]
        except (AttributeError, KeyError):
            abort(404)

        template = conf.build_map[self.name]['template']
        playbook = conf.build_map[self.name]['playbook']

        files_to_compress = []
        rendered_yml = render(template, **kw)
        tmp_dir = tempfile.mkdtemp()
        yml_file = os.path.join(tmp_dir, 'main.yml')
        with open(yml_file, 'w') as f:
            f.write(rendered_yml)
        files_to_compress.append(playbook)
        files_to_compress.append(yml_file)

        playbook = tar_czf(files_to_compress)

        response.headers['Content-Disposition'] = 'attachment; filename=playbook.tar.gz'
        f = open(playbook, 'rb')
        response.app_iter = FileIter(f)


class BuildsController(object):

    @expose()
    def _lookup(self, name, *remainder):
        return BuildController(name), remainder
