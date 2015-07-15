# Server Specific Configurations
server = {
    'port': '8000',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'prado.controllers.root.RootController',
    'modules': ['prado'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/prado/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
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


setup_script = '%(confdir)s/public/setup.sh'
setup_ansible = '%(confdir)s/public/ansible.tar.gz'
playbook = '%(confdir)s/public/playbook.tar.gz'


# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
