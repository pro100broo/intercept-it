from typing import Optional, Union, Type, List

from intercept_it.exceptions import InterceptorException
from intercept_it.models.handlers import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger

from intercept_it.models import GlobalConfig, GroupConfig, UnitConfig
from intercept_it.models.base_config import BaseConfig


class BaseInterceptor:
    def __init__(self, config: Union[GlobalConfig, GroupConfig, UnitConfig]):
        self._config = config
        self._config.sort_handlers()

    def execute_handlers(
        self,
        exception: Exception,
        loggers: Optional[List[BaseLogger]],
        handlers: List[DefaultHandler],
        raise_exception: bool
    ) -> None:

        self._process_loggers(loggers, str(exception))

        [handler.execute() for handler in handlers]

        if raise_exception:
            raise exception

    @staticmethod
    def _process_loggers(loggers: Optional[List[BaseLogger]], message: str) -> None:
        if loggers:
            for logger in loggers:
                logger.save_logs(message)

    @staticmethod
    def _check_config(config: BaseConfig, target_config: Type[BaseConfig]) -> None:
        if not isinstance(config, target_config):
            raise InterceptorException(
                f'Invalid config type: {config.__class__.__name__}. '
                f'Expected {target_config.__name__}'
            )
