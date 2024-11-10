import math

from pydantic import ValidationError

from intercept_it import GroupConfig, GroupProperties, GroupInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler
from intercept_it.utils import WarningLevelsEnum, TimeCooldownsEnum

config = GroupConfig(
    {
        'Math exceptions': GroupProperties(
            [ZeroDivisionError, ValueError],
            loggers=[STDLogger(logging_level=WarningLevelsEnum.WARNING.value)]
        ),
        123: GroupProperties(
            [IndexError, ValidationError],
            loggers=[STDLogger(logging_level=WarningLevelsEnum.ERROR.value)],
            raise_exception=True
        )
    }
)

config.register_handler(
    'Math exceptions',
    lambda message: print(message),
    'Math is so hard...',
    execution_order=1
)

config.register_handler(
    'Math exceptions',
    cooldown_handler,
    TimeCooldownsEnum.FIVE_SECONDS.value,
    execution_order=2
)


config.register_handler(
    123,
    lambda message: print(message),
    'Unexpected list index access!!!',
)

interceptor = GroupInterceptor(config)


@interceptor.handle_exceptions_group('Math exceptions')
def dangerous_calculation1(some_number: int) -> float:
    return some_number / 0


@interceptor.handle_exceptions_group('Math exceptions')
def dangerous_calculation2(some_number: int) -> float:
    return math.sqrt(some_number)


@interceptor.handle_exceptions_group(123)
def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


if __name__ == '__main__':
    dangerous_calculation1(5)
    dangerous_calculation2(-1)
    dangerous_list_access(100)
