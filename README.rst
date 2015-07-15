``prado``
==========
Is a web service that provides a full installation of Ansible over HTTP with
the ability to understand query arguments as playbook variables so that the
playbook to be served will be exactly what a host needs.


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
