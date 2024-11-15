from intercept_it.exceptions import InterceptItSetupException
from intercept_it.loggers.base_logger import BaseLogger
from intercept_it.configs.base_config import BaseConfig


class SetupChecker:
    """ Implements additional checks of interceptor parameters before initialization """
    @staticmethod
    def check_config(config: BaseConfig, target_config: type[BaseConfig]) -> None:
        """ Checks if received configuration class is valid for current ``Interceptor`` """
        if not isinstance(config, target_config):
            raise InterceptItSetupException(
                f'Invalid config type: {config.__class__.__name__}. Expected {target_config.__name__}'
            )

    @staticmethod
    def check_loggers(loggers: list[BaseLogger] | None,) -> None:
        """ Checks if all of received loggers are subclasses of the ``BaseLogger`` """
        if loggers:
            for logger in loggers:
                if not isinstance(logger, BaseLogger):
                    raise InterceptItSetupException(
                        f'Wrong logger setup for {logger.__class__.__name__}. It must implements BaseLogger class'
                    )
