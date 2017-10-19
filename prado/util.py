import os
import json
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
        command = "{} --extra-vars '{}'".format(command, json.dumps(params))
    bash = """#!/bin/bash -x -e
# Do not use sudo for any commands as this script is ran
# by root.
echo "--> do not requiretty for sudoers"
# now allocate a pseudo tty with ssh and fix sudoers
sed -i "s/Defaults    requiretty/#Defaults    requiretty/" /etc/sudoers

build_tar="{address}/build/{name}"

# Define and create a temporary directory for this build
timestamp=`date +%s`
build_dir="prado_$timestamp"
mkdir $build_dir
cd $build_dir

# retrieve the source for this build
curl -u {user}:{key} -s -L -o playbook.tar.gz "$build_tar"
tar xzf playbook.tar.gz
cd playbook
library="`pwd`/library"

ANSIBLE_LIBRARY=$ANSIBLE_LIBRARY:$library {command}
"""
    script = StringIO()
    script.write(
        bash.format(
            address=address,
            command=command,
            name=name,
            user=conf.api_user,
            key=conf.api_key,
        )
    )
    script.seek(0)
    return script
