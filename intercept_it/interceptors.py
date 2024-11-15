from intercept_it.base_interceptor import BaseInterceptor
from intercept_it.utils.setup_checks import SetupChecker
from intercept_it.exceptions import InterceptItException
from intercept_it.configs import (
    GlobalConfig,
    GroupConfig,
    GroupProperties,
    UnitConfig,
)


class GlobalInterceptor(BaseInterceptor, SetupChecker):
    """ Subscribes to specified exceptions and execute the same processing logic for all of them """
    def __init__(self, config: GlobalConfig):
        """
        Process setup checks, then execute initializing of ``BaseInterceptor`` class with config parameters

        :param config: Interceptor's configuration
        """
        self.check_config(config, GlobalConfig)
        self.check_loggers(config.loggers)
        super().__init__(config)

    def handle_exceptions(self, function):
        """
        Wraps target method or function and waits for exceptions specified in ``Config`` class.
        If unspecified exception occurred, raises it again, else intercept it
        """
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as exception:
                if exception.__class__ in self._config.exceptions:
                    self.execute_handlers(
                        exception,
                        self._config.loggers,
                        self._config.handlers,
                        self._config.raise_exception
                    )
                else:
                    raise exception

        return wrapper


class GroupInterceptor(BaseInterceptor, SetupChecker):
    """ Has unique processing logic for every group of exception """
    def __init__(self, config: GroupConfig):
        """
        Process setup checks, then execute initializing of ``BaseInterceptor`` class with config parameters

        :param config: Interceptor's configuration
        """
        self._check_setup(config)
        super().__init__(config)

    def handle_exceptions_group(self, group_id: int | str):
        """
        Wraps target method or function and waits for exceptions specified in ``Config`` class.
        If unspecified exception occurred, raises it again, else intercept it

        :param group_id: Group id, specified in config
        :return:
        """
        def outer(function):
            def wrapper(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except Exception as exception:
                    self._check_group(group_id)
                    if exception.__class__ in self._config.groups[group_id].exceptions:
                        target_group = self._config.groups[group_id]
                        self.execute_handlers(
                            exception,
                            target_group.loggers,
                            target_group.handlers,
                            target_group.raise_exception
                        )
                    else:
                        raise exception
            return wrapper
        return outer

    def _check_group(self, group_id: int | str) -> None:
        if group_id not in self._config.groups:
            raise InterceptItException(f'Intercepted unexpected group: {group_id}')

    def _check_setup(self, config: GroupConfig) -> None:
        """ Call to superclass methods, to check validity of every specified group """
        for group_properties in config.groups.values():
            super().check_config(group_properties, GroupProperties)
            super().check_loggers(group_properties.loggers)


class UnitInterceptor(BaseInterceptor, SetupChecker):
    """
    Subscribes to specific exception with unique processing logic.
    If exception not specified in decorator parameter, intercepts base ``Exception`` class
    """
    def __init__(self, config: UnitConfig):
        """
        Process setup checks, then execute initializing of ``BaseInterceptor`` class with config parameters

        :param config: Interceptor's configuration
        """
        self.check_config(config, UnitConfig)
        self.check_loggers(config.loggers)
        super().__init__(config)

    def handle_exception(self, target_exception: type[Exception] = Exception):
        """
        Wraps target method or function and waits for exceptions specified in ``Config`` class.
        If unspecified exception occurred, raises it again, else intercept it

        :param target_exception: Specify target exception. Default -> Base exception class
        :return:
        """
        def outer(function):
            def wrapper(*args, **kwargs):
                try:
                    return function(*args, **kwargs)
                except Exception as exception:
                    if exception.__class__ == target_exception:
                        self.execute_handlers(
                            exception,
                            self._config.loggers,
                            self._config.handlers,
                            self._config.raise_exception
                        )
                    else:
                        raise exception
            return wrapper
        return outer
