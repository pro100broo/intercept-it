from typing import Callable

from intercept_it.configs.base_config import BaseConfig
from intercept_it.utils.models import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger
from intercept_it.exceptions import InterceptItSetupException


class GlobalConfig(BaseConfig):
    """ Configuration class for ``GlobalInterceptor`` """
    def __init__(
            self,
            exceptions: list[type[Exception]],
            raise_exception: bool = False,
            loggers: list[BaseLogger] | None = None
    ):
        """
        Execute initializing of ``BaseConfig`` class with received parameters

        :param exceptions: List of target exceptions
        :param raise_exception: If equals ``True``, intercepted exception raises further
        :param loggers: List of received loggers
        """
        super().__init__(raise_exception, loggers)
        self.exceptions = exceptions


class GroupProperties(BaseConfig):
    """ Configuration class for ``GroupInterceptor`` """
    def __init__(
            self,
            exceptions: list[type[Exception]],
            raise_exception: bool = False,
            loggers: list[BaseLogger] | None = None
    ):
        """
        Execute initializing of ``BaseConfig`` class with received parameters

        :param exceptions: List of target exceptions
        :param raise_exception: If equals ``True``, intercepted exception raises further
        :param loggers: List of received loggers
        """
        super().__init__(raise_exception, loggers)
        self.exceptions = exceptions


class GroupConfig:
    """ Configuration class for ``GroupInterceptor``. Implements storing of ``GroupProperties`` """
    def __init__(self, groups: dict[int | str, GroupProperties]):
        """
        Receives groups collection

        :param groups: Dictionary with the following structure: {group_id: GroupProperties}
        """
        self.groups = groups

    def register_handler(
            self,
            group_id: int | str,
            attached_callable: Callable,
            *args,
            execution_order: int = 1,
            **kwargs
    ) -> None:
        """
        Overrides ``register_handler`` method of the BaseConfig. Implements similar registration logic for groups

        :param group_id: Group id
        :param attached_callable: Specified callable object
        :param args: Callable positional arguments
        :param execution_order: Callables execution order
        :param kwargs: Callable keyword arguments
        """
        if group_id not in self.groups:
            raise InterceptItSetupException(f'Attempt to register handler to unknown group_id: {group_id}')

        self.groups[group_id].handlers.append(
            DefaultHandler(
                attached_callable=attached_callable,
                execution_order=execution_order,
                args=args,
                kwargs=kwargs
            )
        )
        self.sort_handlers()

    def sort_handlers(self) -> None:
        """
        Overrides ``sort_handlers`` method of the BaseConfig.
        Implements sort of callables execution order in every group
        """
        for group in self.groups.values():
            group.handlers = sorted(group.handlers, key=lambda priority: priority)


class UnitConfig(BaseConfig):
    """ Configuration class for ``UnitInterceptor`` """
    def __init__(
            self,
            raise_exception: bool = False,
            loggers: list[BaseLogger] | None = None
    ):
        """
        Execute initializing of ``BaseConfig`` class with received parameters

        :param raise_exception: If equals ``True``, intercepted exception raises further
        :param loggers: List of received loggers
        """
        super().__init__(raise_exception, loggers)
