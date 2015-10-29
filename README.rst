``prado``
==========
Bootstrap Ansible and a playbook with variables.

prado is a web service that provides a full installation of Ansible and
its dependencies over HTTP, with the ability to understand query arguments
as playbook variables so that the playbook to be served will be exactly
what a host needs when executing.

An example call to the webservice by the host would look like::

    curl -L http://prado.example/setup/myplaybook/ | bash

project name
------------
Usually, running curl from some url and executing the contents with a shell is
frowned upon. Especially when it is across the internet. This is meant to be run
within a protected environment *without* being exposed to the internet.

The name was chosen in honor of Don Damaso Perez Prado, the King of Mambo.
Mambo was forbidden and frowned upon when it appeared. But people still found
a way to enjoy it in closed environments. Just like this service.


When or Why would this be useful?
---------------------------------
When bringing up new hosts, they can call
the HTTP service at a distinct endpoint and get exactly the playbook they need.

Since the API call will have a ready-to-go Ansible source, it will not need to
install anything else (not even dependencies).

Where would something like that work?
-------------------------------------
OpenStack instances allow you to "run a script on boot", same with Amazon AWS
service (as long as the image has cloud-init installed), VMWare, etc...

All these services allow for a script to be run at boot.

The specific use case for this service was to be able to fire up a host and get
that host to register as a Jenkins slave, saving the administrator from the
hassle to go through Jenkins's UI. As soon as the host was ready, Jenkins was
able to start sending jobs to it as a valid slave with executors ready to do
work.


configuring playbooks
=====================
The prado service maps configured, named playbooks to service endpoints.

For example, a build for a Jenkins slave might look like this in a Pecan
config::

    build_map = {
        "slave": {
            "playbook": "%(confdir)s/public/ceph-build/ansible/slaves",
            "template": "%(confdir)s/public/ceph-build/ansible/slaves/slave.yml.j2",
            "command": 'ansible-playbook -i "localhost," -c local ../main.yml'
        }
    }

Which would be reachable at::

    setup/slave/

and all HTTP query args would be passed onto the template file.

templating
----------
To avoid collision with Ansible's support for Jinja2, templates for playbooks
use Mako (http://www.makotemplates.org/).

A simple debug message in a playbook template that looks like::

    - debug: msg="this is a message where ${foo} and ${meh} should be defined"

would get rendered and ready to execute when passing the variables to the
configured endpoint (using 'slave' here as an example)::

    http://0.0.0.0:8000/setup/slave/?foo=1&meh=2

Output of the playbook would show::

    TASK: [debug msg="this is a message where 1 and 2 should be defined"] *******

command
-------
When defining commands, since ansible will actually run on the
target host, you should use ``-i "localhost," -c local`` to
ensure that ansible will use local connections and run on localhost only.

The example above shows ``main.yml``::

    "command": 'ansible-playbook -i "localhost," -c local ../main.yml'

Also note: when the template playbook is expanded, the output is named
``main.yml`` and added to the top level of the compressed directory so
that the script has a reliable way to find it. Since the script also
changes directories to where the playbook files are, that means that the
``main.yml`` file will always need to be reached on the parent directory.

custom modules
--------------
Custom Ansible modules are supported as long as they exist within the playbook
in a ``library`` directory. When the playbook executes it will always append
the full path to the playbook library directory (even if it doesn't exist) as
a convenience feature.
