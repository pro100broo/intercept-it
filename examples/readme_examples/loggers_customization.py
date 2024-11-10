from intercept_it import GlobalConfig, GlobalInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler
from intercept_it.utils import WarningLevelsEnum, TimeCooldownsEnum


def custom_formatter(message: str) -> str:
    return f'I was formatted: {message}'


# Default std logger
default_logger = STDLogger()

# Customized std logger
customized_logger = STDLogger(
    logging_level=WarningLevelsEnum.INFO.value,
    default_formatter=custom_formatter,
    pytz_timezone='Africa/Tunis',
)

# Initialize interceptor's config class
config = GlobalConfig(
    [IndexError, ZeroDivisionError],  # Collection of subscribed exceptions
    loggers=[default_logger, customized_logger],  # Use default std logger
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
