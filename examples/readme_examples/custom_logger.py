import logging

from intercept_it import GlobalConfig, GlobalInterceptor
from intercept_it.loggers.base_logger import BaseLogger

from intercept_it.utils import cooldown_handler
from intercept_it.utils import TimeCooldownsEnum


class CustomLogger(BaseLogger):
    def __init__(self):
        self._logger = logging.getLogger()

    def save_logs(self, message: str) -> None:
        self._logger.warning(f'Be careful! Im custom logger: {message}')


custom_logger = CustomLogger()

# Initialize interceptor's config class
config = GlobalConfig(
    [IndexError, ZeroDivisionError],  # Collection of subscribed exceptions
    loggers=[custom_logger],  # Use default std logger
)

# Add some handlers to config
config.register_handler(
    cooldown_handler,  # callable
    TimeCooldownsEnum.FIVE_SECONDS.value,  # positional argument
    execution_order=1
)

config.register_handler(
    lambda x, y: print(f'{x}. {y}'),  # another callable :)
    'I am additional handler', 'It is so cool!',  # a few positional arguments
    execution_order=2
)

# Now we can initialize interceptor object with necessary configuration
interceptor = GlobalInterceptor(config)


# Intercept the exceptions!
@interceptor.handle_exceptions
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


# Intercept the exceptions!
@interceptor.handle_exceptions
def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


if __name__ == '__main__':
    dangerous_calculation(5)
    dangerous_list_access(100)
