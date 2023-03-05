from service_api.configs import RuntimeConfig


logger_configs = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std_format": {
            "format": "[%(asctime)s %(name)s] [%(levelname)s] [%(module)s:%(funcName)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": RuntimeConfig.log_level,
            "formatter": "std_format",
        }
    },
    "loggers": {
        "app_logger": {
            "level": RuntimeConfig.log_level,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
