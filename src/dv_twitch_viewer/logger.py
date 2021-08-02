import logging
import logging.config

import structlog

from settings import settings


def configure_logger():
    """Configure the logger to use throughout the project

    Uses these variables from settings:
        LOG_LEVEL -- The loglevel to use
    """

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters':
            {
                'default':
                    {
                        'format': '[%(levelname)s] %(name)s: %(message)s'
                    }
            },
        'handlers':
            {
                'stdout':
                    {
                        'class': 'logging.StreamHandler',
                        'formatter': 'default',
                        'stream': 'ext://sys.stdout'
                    }
            },
        'loggers':
            {
                '':
                    {
                        'handlers': ['stdout'],
                        'level': 'DEBUG',
                        'propagate': True
                    }
            }
    })
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Returns a logger object with proper name

    Parameters
    ----------
    name : str
        name of the logger

    Returns
    -------
    logging.Logger
        logger object
    """
    return structlog.get_logger(f"dv.{name}")
