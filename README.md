## Intercept-it library
The philosophy of the library is the ability to flexibly catch any exception,  
execute some logic specified for this exception and continue executing the program.

### Features
* Different ways to intercept exceptions
* Easy setup of interceptors objects
* Using interceptors with decorators does not affect the readability of the code
* Generic logging system:
  * Built-in std and telegram loggers
  * Easy way to create and use custom loggers
  * Supports the use of several loggers for the one exception
* Generic handlers:
  * Built-in handlers
  * Use any callable such as default function, lambda function or complete class with any arguments
  * Choose execution order of the handlers. Handlers will be automatically sorted by this order

## Installation guide (GitHub)
#### 1. Clone the project repo one of the following ways:
```console
$ git clone https://github.com/pro100broo/intercept-it.git
$ git clone git@github.com/pro100broo/intercept-it.git
```

#### 2. Jump into the project repository
```console
$ cd intercept-it
```

#### 3. Create and activate python virtual environment
```console
$ python3 -m venv venv
$ source venv/bin/acitvate
```

#### 4. Install setuptools
```console
$ pip3 install setuptools
```

#### 4. Install the library one of the following ways:
```console
$ make app-build
$ make app-build-clean
$ python3 setup.py install
```

## Installation guide (pip)
```console
$ pip install intercept-it
```

## Usage example
There are three main classes to intercept exceptions:

1. ``GlobalInterceptor`` - subscribes to specified exceptions and execute the same processing logic for all of them
2. ``GroupInterceptor`` - divides specified exceptions into groups with unique processing logic
3. ``UnitInterceptor`` - subscribes to specific exception with unique processing logic

Before using, you need to set up them with specific config class


### Let's see how to configure and use GlobalInterceptor!
```python
from intercept_it import GlobalConfig, GlobalInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler
from intercept_it.utils import TimeCooldownsEnum

# Initialize interceptor's config class
config = GlobalConfig(
    [IndexError, ZeroDivisionError],  # Collection of subscribed exceptions
    loggers=[STDLogger()],  # Use default std logger
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

```
### Execution results:

```console
2024-11-10 17:49:33.156556+03:00 | ERROR | File "...\intercept-it\examples\readme_examples\global_example.py", line 45: division by zero
I am additional handler. It is so cool!
2024-11-10 17:49:38.174263+03:00 | ERROR | File "...\intercept-it\examples\readme_examples\global_example.py", line 46: list index out of range
I am additional handler. It is so cool!
```
We used two simple handlers:

* Default cooldown handler (just waits the specified time after intercepting the exception)
* Simple lambda function with some logging message

You can execute more difficult logic such as sending exception details to logs stash or notify clients in messengers

Other Interceptors have quite different setup. You can find additional usage examples [here](https://github.com/pro100broo/intercept-it/tree/main/examples)

## Usage tips

### Loggers customization:

```python
from intercept_it import GlobalConfig
from intercept_it.loggers import STDLogger
from intercept_it.utils import WarningLevelsEnum

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

# Initialize interceptor's config class with a few loggers
config = GlobalConfig(
    [IndexError, ZeroDivisionError],  
    loggers=[default_logger, customized_logger],  
)
```
```console
2024-11-10 15:55:28.415905+01:00 | ERROR | File "...\intercept-it\examples\readme_examples\loggers_customization.py", line 59: division by zero
2024-11-10 15:55:28.415905+01:00 | INFO | I was formatted: division by zero
I am additional handler. It is so cool!
2024-11-10 15:55:33.428577+01:00 | ERROR | File "...\intercept-it\examples\readme_examples\loggers_customization.py", line 60: list index out of range
2024-11-10 15:55:33.428577+01:00 | INFO | I was formatted: list index out of range
I am additional handler. It is so cool!
```

### Creating new loggers:

Each logger must be an instance of the ``BaseLogger`` class. It implements only one method: ``save_logs``

```python
import logging

from intercept_it import GlobalConfig
from intercept_it.loggers.base_logger import BaseLogger

# Custom logger
class CustomLogger(BaseLogger):
    def __init__(self):
        self._logger = logging.getLogger()

    def save_logs(self, message: str) -> None:
        self._logger.warning(f'Be careful! Im custom logger: {message}')
 

# Initialize interceptor's config class
config = GlobalConfig(
    [IndexError, ZeroDivisionError],  # Collection of subscribed exceptions
    loggers=[CustomLogger()],  # Use default std logger
)

```
```console
Be careful! Im custom logger: division by zero
I am additional handler. It is so cool!
Be careful! Im custom logger: list index out of range
I am additional handler. It is so cool!
```

### Exceptions management:

If you need to send further caught exception or implement nested interceptors, you need specify 
``raise_exception`` parameter of any configuration class

```python
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


@unit_interceptor.handle_exception(target_exception=ZeroDivisionError)
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
```
```console
Got exception in third-party function
Got exception in main function
Got exception in entry point
```
