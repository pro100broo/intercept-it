from intercept_it import GlobalConfig, GlobalInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler, resuming_handler
from intercept_it.utils import TimeCooldownsEnum, ResumeFlagsEnum
from intercept_it.exceptions import ContinueProgramException

config = GlobalConfig(
    [IndexError, ZeroDivisionError],
    loggers=[STDLogger()],
)

config.register_handler(
    cooldown_handler,
    TimeCooldownsEnum.FIVE_SECONDS.value,
    execution_order=1
)

config.register_handler(
    lambda x, y: print(f'{x}. {y}'),
    'I am additional handler', 'It is so cool!',
    execution_order=2
)

config.register_handler(
    resuming_handler,
    ResumeFlagsEnum.CONTINUE_EXECUTION.value,
    execution_order=3
)

interceptor = GlobalInterceptor(config)


@interceptor.handle_exceptions
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


@interceptor.handle_exceptions
def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


if __name__ == '__main__':
    while True:
        try:
            dangerous_calculation(5)
        except ContinueProgramException:
            pass

        try:
            dangerous_list_access(100)
        except ContinueProgramException:
            pass
