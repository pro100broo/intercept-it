from typing import Optional, List, Callable, Union

from intercept_it.utils.models import DefaultHandler
from intercept_it.loggers.base_logger import BaseLogger


class BaseConfig:
    """ Base config implements shared logic for all concrete configs """
    def __init__(
        self,
        raise_exception: bool = False,
        loggers: Optional[List[BaseLogger]] = None
    ):
        """
        :param raise_exception: If equals ``True``, intercepted exception raises further
        :param loggers: Specified loggers
        """
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
        """
        Adds some callable to the specified ``Config`` class

        :param attached_callable: Specified callable object
        :param args: Callable positional arguments
        :param execution_order: Callables execution order
        :param kwargs: Callable keyword arguments
        """
        self.handlers.append(
            DefaultHandler(
                attached_callable=attached_callable,
                execution_order=execution_order,
                args=args,
                kwargs=kwargs
            )
        )
        self.sort_handlers()

    def sort_handlers(self) -> None:
        """ Sorts handlers by ``execution_order`` parameter """
        self.handlers = sorted(self.handlers, key=lambda priority: priority)
