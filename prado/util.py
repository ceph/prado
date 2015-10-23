import os
from urllib import urlencode
from StringIO import StringIO
import tempfile
import tarfile
from pecan import conf
from mako.lookup import TemplateLookup
# TODO: need to parse mako errors/exceptions so that the client can understand
# when/how things are not working
# from mako.exceptions import (CompileException, SyntaxException,
#                             html_error_template)


def render(path, **params):
    loader = TemplateLookup(
        directories=[os.path.dirname(path)],
        output_encoding='utf-8'
    )
    tmpl = loader.get_template(os.path.basename(path))
    return tmpl.render(**params)


def tar_czf(paths):
    tmp_dir = tempfile.gettempdir()
    output_filename = os.path.join(tmp_dir, 'playbook.tar.gz')

    with tarfile.open(output_filename, "w:gz") as tar:
        for path in paths:
            # we are being naive here, assuming one yml file as a template
            # and a directory as the playbook
            if os.path.isdir(path):
                arcname = 'playbook'
            else:
                arcname = os.path.basename(path)
            tar.add(path, arcname=arcname)
    return output_filename


def make_setup_script(name, **params):
    # blow up if the command is not defined
    command = conf.build_map[name]['command']
    address = conf.service_address.strip('/')
    if params:
        encoded = "?%s" % urlencode(params)
    else:
        encoded = ""
    bash = """#!/bin/bash -x -e
# Make sure we can sudo without a prompt:
# create the ssh key and slap it into authorized_keys
# so we can ssh into localhost
echo "--> generating ssh keys"
echo -e  "y\\n" | ssh-keygen -q -t rsa -N "" -f ~/.ssh/id_rsa

echo "--> copying local public key into authorized_keys"
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

echo "--> allocating pseudo tty with ssh to fix sudoers"
# now allocate a pseudo tty with ssh and fix sudoers
ssh -n -t -t -o 'StrictHostKeyChecking=no' localhost 'sudo sed -i "s/Defaults    requiretty/#Defaults    requiretty/" /etc/sudoers' &

echo "--> getting ready to fetch ansible"
build_tar="{address}/build/{name}{encoded}"
ansible_tar="{address}/setup/ansible/"

# Define and create a temporary directory for this build
timestamp=`date +%s`
build_dir="prado_$timestamp"
mkdir $build_dir
cd $build_dir

# retrieve the pre-made ansible source and untar
curl -u {user}:{key} -s -L -o ansible.tar.gz "$ansible_tar"
tar xzf ansible.tar.gz

# retrieve the source for this build
curl -u {user}:{key} -s -L -o playbook.tar.gz "$build_tar"
tar xzf playbook.tar.gz
cd playbook
library="`pwd`/library"

ANSIBLE_LIBRARY=$ANSIBLE_LIBRARY:$library bash ../build/bin/{command}
"""
    script = StringIO()
    script.write(
        bash.format(
            address=address,
            command=command,
            name=name,
            encoded=encoded,
            user=conf.api_user,
            key=conf.api_key,
        )
    )
    script.seek(0)
    return script
