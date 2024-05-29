import logging.config
import logging.handlers

LOG_FILE = 'logs/log.log'
ERROR_FILE = 'logs/error.log'
DEBUG_FILE = 'logs/debug.log'

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s %(message)s]',
        },
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'terminal': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'simple'
        },
        'log_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.INFO,
            'filename': LOG_FILE,
            'formatter': 'detail',
            'mode': 'a'
        },
        'debug_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.INFO,
            'filename': DEBUG_FILE,
            'formatter': 'detail',
            'mode': 'a'
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.WARN,
            'filename': ERROR_FILE,
            'formatter': 'detail',
            'mode': 'a'
        },
    },
    'loggers': {
        'base_logger': {
            'handlers': ['terminal', 'log_file'],
            'level': logging.INFO,
            'handeException': False,
            'exitOnError': False,
            'propagate': False,
        },
        'debug_logger': {
            'handlers': ['terminal', 'debug_file'],
            'level': logging.DEBUG,
            'handeException': False,
            'exitOnError': False,
            'propagate': False,
        },
        'error_logger': {
            'handlers': ['terminal', 'error_file'],
            'level': logging.WARNING,
            'handeException': True,
            'exitOnError': True,
            'propagate': False,
        },
    },
})

error_logger = logging.getLogger('error_logger')
debug_logger = logging.getLogger('debug_logger')
base_logger = logging.getLogger('base_logger')
