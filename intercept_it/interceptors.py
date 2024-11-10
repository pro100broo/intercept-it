from typing import Union, Type

from intercept_it.base_interceptor import BaseInterceptor
from intercept_it.exceptions import InterceptorException
from intercept_it.models.configs import (
    GlobalConfig,
    GroupConfig,
    GroupProperties,
    UnitConfig,
)


class GlobalInterceptor(BaseInterceptor):
    def __init__(self, config: GlobalConfig):
        self._check_config(config, GlobalConfig)
        super().__init__(config)

    def handle_exceptions(self, function):
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


class GroupInterceptor(BaseInterceptor):
    def __init__(self, config: GroupConfig):
        self._check_config(config, GroupConfig)
        super().__init__(config)

    def handle_exceptions_group(self, group_id: Union[int, str]):
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

    def _check_group(self, group_id: Union[int, str]) -> None:
        if group_id not in self._config.groups:
            raise InterceptorException(f'Intercepted unexpected group_id: {group_id}')

    def _check_config(self, config: GroupConfig, target_config: Type[GroupConfig]):
        for _, group_properties in config.groups.items():
            super()._check_config(group_properties, GroupProperties)


class UnitInterceptor(BaseInterceptor):
    def __init__(self, config: UnitConfig):
        self._check_config(config, UnitConfig)
        super().__init__(config)

    def handle_exception(self, target_exception: Type[Exception]):
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
