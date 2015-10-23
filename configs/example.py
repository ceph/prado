# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'prado.controllers.root.RootController',
    'modules': ['prado'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/prado/templates',
    'debug': True,
}

logging = {
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'prado': {'level': 'DEBUG', 'handlers': ['console']},
        'pecan': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                       '[%(threadName)s] %(message)s'),
        '__force_dict__': True
        }
    }
}


setup_ansible = '%(confdir)s/public/ansible.tar.gz'

build_map = {
# a build_map entry defines what is available to be served, it is required that each
# playbook has an entry here defining the commands needed to run
#    "slave": {
#        "playbook": "%(confdir)s/public/ceph-build/ansible/slaves",
#        "template": "%(confdir)s/public/ceph-build/ansible/slaves/slave.yml.j2",
#        "command": 'ansible-playbook -i "localhost," -c local ../main.yml'
#    }
}

# if we are getting proxied by say, NGINX we can't use the server port and
# address for the app itself so this needs to be defined again here
service_address = 'http://localhost:8080'

# these are used to access the service, via Basic HTTP Auth
api_user = 'admin'
api_key = 'secret'
