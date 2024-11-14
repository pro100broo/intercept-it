from typing import Callable, Tuple, Dict
from pydantic import BaseModel


class DefaultHandler(BaseModel):
    attached_callable: Callable
    execution_order: int
    args: Tuple
    kwargs: Dict

    def execute(self):
        self.attached_callable(*self.args, **self.kwargs)

    def __gt__(self, other) -> bool:
        return self.execution_order > other.execution_order

