from pecan import expose, response, redirect, conf, abort
from webob.static import FileIter


class SetupController(object):

    @expose(content_type='application/octet-stream', generic=True)
    def index(self):
        """
        Special method for internal redirect URI's so that webservers (like
        Nginx) can serve downloads to clients while the app just delegates.
        This method will require an Nginx configuration that points to
        resources and match `binary_root` URIs::

            location /home/ubuntu/repos/ {
              internal;
              alias   /files/;
            }

        `alias` can be anything, it would probably make sense to have a set of
        rules that allow distinct URIs, like::

            location /home/ubuntu/repos/rpm-firefly/ {
              internal;
              alias   /files/rpm-firefly/;
            }


        There are two ways to get binaries into this app: via existing files in
        certain paths POSTing JSON to the arch/ endpoint, or via actual upload
        of the binary. So if many locations need to be supported, they each
        need to have a corresponding section in Nginx to be configured.
        """
        # we need to slap some headers so Nginx can serve this
        # XXX Maybe we don't need to set Content-Disposition here?
        response.headers['Content-Disposition'] = 'attachment; filename=setup.sh'
        response.headers['X-Accel-Redirect'] = conf.setup_script
        f = open(conf.setup_script, 'rb')
        response.app_iter = FileIter(f)

    @expose(content_type='application/octet-stream', generic=True)
    def ansible(self):
        response.headers['Content-Disposition'] = 'attachment; filename=ansible.tar.gz'
        response.headers['X-Accel-Redirect'] = conf.setup_script
        f = open(conf.setup_ansible, 'rb')
        response.app_iter = FileIter(f)

