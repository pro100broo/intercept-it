from typing import Optional, List, Callable, Union

from intercept_it.models.handlers import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger


class BaseConfig:
    def __init__(
        self,
        raise_exception: bool = False,
        loggers: Optional[List[BaseLogger]] = None
    ):
        self.raise_exception = raise_exception
        self.loggers = loggers
        self.handlers = []

    def register_handler(
            self,
            attached_callable: Callable,
            *args,
            execution_order: Union[int, str] = 1,
            **kwargs
    ) -> None:
        self.handlers.append(
            DefaultHandler(
                attached_callable=attached_callable,
                execution_order=execution_order,
                args=args,
                kwargs=kwargs
            )
        )

    def sort_handlers(self) -> None:
        self.handlers = sorted(self.handlers, key=lambda priority: priority)
