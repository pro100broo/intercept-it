from intercept_it import UnitConfig, UnitInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler
from intercept_it.utils import TimeCooldownsEnum

config = UnitConfig(loggers=[STDLogger()])

config.register_handler(
    cooldown_handler,
    TimeCooldownsEnum.FIVE_SECONDS.value,
)

interceptor = UnitInterceptor(config)


@interceptor.handle_exception(target_exception=ZeroDivisionError)
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


@interceptor.handle_exception(target_exception=IndexError)
def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


if __name__ == '__main__':
    dangerous_calculation(5)
    dangerous_list_access(100)
