import logging.config

from service_api.services.logger.configs import logger_configs


logging.config.dictConfig(logger_configs)
app_logger = logging.getLogger("app_logger")
