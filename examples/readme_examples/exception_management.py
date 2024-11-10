from intercept_it import GlobalConfig, GlobalInterceptor, UnitConfig, UnitInterceptor

# Setup global interceptor
global_config = GlobalConfig(
    [IndexError, ZeroDivisionError],
    raise_exception=True
)


global_config.register_handler(
    lambda message: print(message),
    'Got exception in main function',
)

global_interceptor = GlobalInterceptor(global_config)

# Setup unit interceptor
unit_config = UnitConfig(
    raise_exception=True
)

unit_config.register_handler(
    lambda message: print(message),
    'Got exception in third-party function',
)

unit_interceptor = UnitInterceptor(unit_config)


@unit_interceptor.handle_exception(ZeroDivisionError)
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


@global_interceptor.handle_exceptions
def main():
    dangerous_calculation(100)


if __name__ == '__main__':
    try:
        main()
    except ZeroDivisionError:
        print('Got exception in entry point')