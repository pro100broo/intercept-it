from typing import Optional, List, Dict, Union, Callable

from intercept_it.models.base_config import BaseConfig
from intercept_it.models.handlers import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger
from intercept_it.exceptions import InterceptorException


class GlobalConfig(BaseConfig):
    def __init__(
            self,
            exceptions: List[type[Exception]],
            raise_exception: bool = False,
            loggers: Optional[List[BaseLogger]] = None
    ):
        super().__init__(raise_exception, loggers)
        self.exceptions = exceptions


class GroupProperties(BaseConfig):
    def __init__(
            self,
            exceptions: List[type[Exception]],
            raise_exception: bool = False,
            loggers: Optional[List[BaseLogger]] = None
    ):
        super().__init__(raise_exception, loggers)
        self.exceptions = exceptions


class GroupConfig:
    def __init__(self, groups: Dict[Union[int, str], GroupProperties]):
        self.groups = groups

    def register_handler(
            self,
            group_id: Union[int, str],
            attached_callable: Callable,
            *args,
            execution_order: Union[int, str] = 1,
            **kwargs
    ) -> None:
        if group_id not in self.groups:
            raise InterceptorException(f'Attempt to register handler to unknown group_id: {group_id}')

        self.groups[group_id].handlers.append(
            DefaultHandler(
                attached_callable=attached_callable,
                execution_order=execution_order,
                args=args,
                kwargs=kwargs
            )
        )

    def sort_handlers(self) -> None:
        for group in self.groups.values():
            group.handlers = sorted(group.handlers, key=lambda priority: priority)


class UnitConfig(BaseConfig):
    pass
