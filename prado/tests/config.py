from prado.hooks import error

# Server Specific Configurations
server = {
    'port': '8000',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'prado.controllers.root.RootController',
    'modules': ['prado'],
    'debug': False,
    'hooks': [error.CustomErrorHook()],
}

logging = {
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'prado': {'level': 'DEBUG', 'handlers': ['console']},
        'pecan.commands.serve': {'level': 'DEBUG', 'handlers': ['console']},
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

# When True it will set the headers so that Nginx can serve the download
# instead of Pecan.
delegate_downloads = False

build_map = {
    "slave": {
        "playbook": "%(confdir)s/../public/ceph-build/ansible",
        "template": "%(confdir)s/../public/ceph-build/ansible/slave.yml.j2",
        "command": 'ansible-playbook -i "localhost," -c local ../main.yml',
    },
    "vars": {
        "playbook": "%(confdir)s/../public/playbook",
        "template": "%(confdir)s/../public/playbook/vars.yml",
        "command": 'ansible-playbook -i "localhost," -c local ../main.yml',
    },
    "novars": {
        "playbook": "%(confdir)s/../public/playbook",
        "template": "%(confdir)s/../public/playbook/no-vars.yml",
        "command": 'ansible-playbook -i "localhost," -c local ../main.yml',
    }
}

setup_ansible = '%(confdir)s/public/ansible.tar.gz'

# FIXME: we need a way to programatically know what IP/address we are serving
# from
service_address = 'http://172.18.181.11'
