from typing import Optional, Union, List

from intercept_it.utils.models import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger

from intercept_it.configs import GlobalConfig, GroupConfig, UnitConfig


class BaseInterceptor:
    """ Base interceptor implements shared logic for all concrete interceptors """
    def __init__(self, config: Union[GlobalConfig, GroupConfig, UnitConfig]):
        """
        :param config: Interceptor's configuration
        """
        self._config = config
        self._config.sort_handlers()

    def execute_handlers(
        self,
        exception: Exception,
        loggers: Optional[List[BaseLogger]],
        handlers: List[DefaultHandler],
        raise_exception: bool
    ) -> None:
        """
        Process specified loggers and handlers when an exception is intercepted

        :param exception: Intercepted exception
        :param loggers: Specified loggers
        :param handlers: Specified handlers
        :param raise_exception: If equals ``True``, intercepted exception raises further
        """
        self._process_loggers(loggers, str(exception))

        [handler.execute() for handler in handlers]

        if raise_exception:
            raise exception

    @staticmethod
    def _process_loggers(loggers: Optional[List[BaseLogger]], message: str) -> None:
        """
        Executes specified loggers with received message

        :param loggers: List of loggers
        :param message: Exception message
        """
        if loggers:
            for logger in loggers:
                logger.save_logs(message)
