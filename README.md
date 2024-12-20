## Intercept-it!
The philosophy of the library is the ability to flexibly catch any exception,  
execute some logic specified for this exception and continue executing the program.

You can intercept exceptions from coroutines and ordinary functions using the same user's interface 

### Features
* Different ways to intercept exceptions
* Easy setup of interceptors objects
* Interceptors can be executed in asynchronous code 
* Generic logging system:
  * Built-in std logger
  * Easy way to create and use custom loggers
  * Supports the use of several loggers for the one exception
* Generic handlers:
  * Use any callable such as default function, lambda function or complete class with any arguments
  * Choose execution order of the handlers
* Maximum customization of any object such as loggers, handlers and interceptors

## Installation guide (pip)

```console
$ pip3 install intercept-it
```

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

#### 3. If you have no python virtual environment, create and activate it 
```console
$ python3 -m venv venv
$ chmod +x venv/bin/activate
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

## Table of contents

### Interceptors overview

#### There are three main classes to intercept exceptions:

1. ``UnitInterceptor`` - Catches specified exception from a function
2. ``GlobalInterceptor`` - Has the ability to catch multiple specified exceptions from a function
3. ``LoopedInterceptor`` - Retry execution of the target function if an exception was caught
4. ``NestedtInterceptor`` - Is a container for few interceptors. Routes any calls to them

Any of them can intercept exceptions in **asynchronous** code too

#### All interceptors have three user interfaces:

* register_handler - Adds any callable handler to interceptor
* intercept - A decorator that catches exceptions
* wrap - A function that can wrap another function to catch exception within it

### Let's see how to configure and use Global Interceptor!
```python
from intercept_it import GlobalInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler


# Initialize interceptor's class with necessary parameters
interceptor = GlobalInterceptor(
    [IndexError, ZeroDivisionError],  # Collection of target exceptions
    loggers=[STDLogger()]  # Use default std logger
)

# Add some handlers to interceptor
interceptor.register_handler(
    cooldown_handler,  # callable
    5,  # positional argument
    execution_order=1
)

interceptor.register_handler(
    lambda x, y: print(f'{x}. {y}'),  # another callable :)
    'I am additional handler', 'It is so cool!',  # a few positional arguments
    execution_order=2
)


# Intercept the exception in decorator
@interceptor.intercept
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


if __name__ == '__main__':
    dangerous_calculation(5)

    # Intercept the exception in wrapper
    interceptor.wrap(dangerous_list_access, 100)

```
#### Results:

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

Other Interceptors have quite different setup. You can find additional usage examples [here](https://github.com/pro100broo/intercept-it/tree/main/examples) or in the following
documentation examples

## Usage tips

### Loggers customization

```python
from intercept_it import GlobalInterceptor
from intercept_it.loggers import STDLogger

# Need to be a function, that receives and returns the string
def custom_formatter(message: str) -> str:
    return f'I was formatted: {message}'


# Default std logger
default_logger = STDLogger()

# Customized std logger
customized_logger = STDLogger(
    logging_level='WARNING',
    default_formatter=custom_formatter,
    pytz_timezone='Africa/Tunis',
)

interceptor = GlobalInterceptor(
    [IndexError, ZeroDivisionError],  
    loggers=[default_logger, customized_logger],  
)
```
#### Results:
```
2024-11-10 15:55:28.415905+01:00 | ERROR | File "...\intercept-it\examples\loggers_customization.py", line 59: division by zero
2024-11-10 15:55:28.415905+01:00 | WARNING | I was formatted: division by zero
2024-11-10 15:55:33.428577+01:00 | ERROR | File "...\intercept-it\examples\loggers_customization.py", line 60: list index out of range
2024-11-10 15:55:33.428577+01:00 | WARNING | I was formatted: list index out of range
```

### Creating new loggers

Each logger must be an instance of the ``BaseLogger`` or ``AsyncBaseLogger`` class and implements ``save_logs`` method

```python
import logging

from intercept_it import GlobalInterceptor
from intercept_it.loggers.base_logger import BaseLogger


# Custom logger
class CustomLogger(BaseLogger):
    def __init__(self):
        self._logger = logging.getLogger()

    def save_logs(self, message: str) -> None:
        self._logger.warning(f'Be careful! Im custom logger: {message}')


interceptor = GlobalInterceptor(
    [IndexError, ZeroDivisionError],  
    loggers=[CustomLogger()],  
)

```
#### Results:
```
Be careful! Im custom logger: division by zero
I am additional handler. It is so cool!
Be careful! Im custom logger: list index out of range
I am additional handler. It is so cool!
```

### Exceptions management

If you need to send intercepted exception higher up the call stack or implement nested interceptors, you need specify 
``raise_exception`` parameter

```python
from intercept_it import GlobalInterceptor, UnitInterceptor

# Setup global interceptor
global_interceptor = GlobalInterceptor(
    [IndexError, ZeroDivisionError],
    raise_exception=True
)

global_interceptor.register_handler(
    lambda message: print(message),
    'Got exception in main function',
)

# Setup unit interceptor
unit_interceptor = UnitInterceptor(
    raise_exception=True
)

unit_interceptor.register_handler(
    lambda message: print(message),
    'Got exception in third-party function',
)


@unit_interceptor.intercept(ZeroDivisionError)
def dangerous_calculation(some_number: int) -> float:
    return some_number / 0


@global_interceptor.intercept
def main():
    dangerous_calculation(100)


if __name__ == '__main__':
    try:
        main()
    except ZeroDivisionError:
        print('Got exception in entry point')
        
```
#### Results:
```
Got exception in third-party function
Got exception in main function
Got exception in entry point
```

### Looping

Let's imagine the situation:
Your script delivers important data from the API to the database every 30 minutes.  
Suddenly, with the next request to the API you get 404 error. For example API server down to maintenance.  
You can use ``LoopedInterceptor`` with specified timeout and wait until the server reboots.

```python
import random

from intercept_it import LoopedInterceptor
from intercept_it import STDLogger


class RequestsException(Exception):
    pass


# Initialize interceptor's object with necessary configuration
interceptor = LoopedInterceptor(
    exceptions=[RequestsException],
    loggers=[STDLogger(default_formatter=lambda error: f'Error occurred: {error}. Waiting for success connection')],
    timeout=5
)


# Simulating the webserver work
@interceptor.intercept
def receive_data_from_api(api_key: str) -> dict[str, str]:
    is_server_down = random.randint(0, 10)
    if is_server_down >= 4:
        raise RequestsException('Integration down to maintenance')

    print(f'Successful connection with api key: {api_key}')
    return {'user': 'pro100broo', 'password': '12345'}


if __name__ == '__main__':
    print(f'Received data from integration: {receive_data_from_api("_API_KEY_")}')
```
#### Results:
```
2024-11-18 01:02:39.596949+03:00 | ERROR | Error occurred: Integration down to maintenance. Waiting for success connection
2024-11-18 01:02:44.597286+03:00 | ERROR | Error occurred: Integration down to maintenance. Waiting for success connection
2024-11-18 01:02:44.597286+03:00 | ERROR | Error occurred: Integration down to maintenance. Waiting for success connection
Successful connection with api key: _API_KEY_
Received data from integration: {'user': 'pro100broo', 'password': '12345'}
```

### Additional processing of wrapped function parameters

Let's imagine another situation :)  
You are developing a service where some data needs to be delivered anyway. 
For example, it can be a chat messanger.  
We take the necessary data from the task pool and try to send messages.  
If the message was not delivered due to a broken connection, you must resend it, returning the data to the additional
task pool.  
You can use any interceptor to route parameters from wrapped function to handlers. 

There are two steps to implement this:

1. Specify ``greed_mode`` parameter for interceptor
2. Specify ``receive_parameters`` parameter for handler

I would recommend to set up and initialize interceptors in separated modules.  
This will make the business logic cleaner and simpler :)

#### Some entities are initialized in an additional module:
```python
# entities.py
import asyncio
import logging
from datetime import datetime
from pydantic import BaseModel

from intercept_it import UnitInterceptor
from intercept_it.loggers.base_logger import BaseAsyncLogger


# Custom exception
class RequestsException(Exception):
    pass


# Custom async logger
class CustomLogger(BaseAsyncLogger):
    def __init__(self):
        self._logger = logging.getLogger()

    async def save_logs(self, message: str) -> None:
        self._logger.error(f"{message} | {datetime.now()}")


# Custom message model
class MessageModel(BaseModel):
    message: str
    status: str

    def __str__(self) -> str:
        return f"Text: {self.message}. Status: {self.status}"


# The stash of undelivered  messages
resend_requests_queue = asyncio.Queue(maxsize=50)


# Undelivered messages handler
async def parameters_handler(message: MessageModel, send_requests_queue: asyncio.Queue) -> None:
    send_requests_queue.task_done()
    print(f'Intercepted message: {message}')
    message.status = 'Awaiting resend'
    await resend_requests_queue.put(message)


# Initialize interceptor's object with necessary configuration
interceptor = UnitInterceptor(
    loggers=[CustomLogger()],
    greed_mode=True,  # Enable routing parameters from the wrapped function to handlers
    async_mode=True  # Enable async code support
)


interceptor.register_handler(
    parameters_handler,
    receive_parameters=True  # Enable receiving wrapped function parameters from interceptor
)
```

####  The main module:
```python
# parameters_processing.py
import random
import asyncio

from entities import (
    MessageModel,
    RequestsException,
    interceptor,
    resend_requests_queue
)


# Attempt to send message
@interceptor.intercept(RequestsException)
async def send_message_to_server(message: MessageModel, tasks_queue: asyncio.Queue) -> None:
    is_server_down = random.randint(0, 10)
    if is_server_down == 10:
        raise RequestsException(f'Connection lost. Failed to send message: {message}')

    message.status = 'Delivered'
    tasks_queue.task_done()

    print(f'Message successfully delivered: {message}')


# Gets message from the queue and tries to send it
async def send_message(send_requests_queue: asyncio.Queue) -> None:
    while True:
        message_content = await send_requests_queue.get()
        await send_message_to_server(message_content, send_requests_queue)


# Simulating the appearance of messages
async def generate_messages(send_requests_queue: asyncio.Queue) -> None:
    [
        await send_requests_queue.put(
            MessageModel(
                message=random.choice(['Hi!', 'Hello!', "What's up!"]),
                status="Awaiting send"
            )
        ) for _ in range(20)
    ]


# The entrypoint
async def main():
    send_requests_queue = asyncio.Queue(maxsize=50)
    await generate_messages(send_requests_queue)

    tasks = [asyncio.create_task(send_message(send_requests_queue)) for _ in range(4)]

    await send_requests_queue.join()

    [task.cancel() for task in tasks]

    print(f'Message queue for sending: {send_requests_queue}')
    print(f'Message queue for resending: {resend_requests_queue}')


if __name__ == '__main__':
    asyncio.run(main())
```
#### Results:
```
Connection lost. Failed to send message: Text: Hi!. Status: Awaiting send | 2024-11-18 03:22:30.645844
Connection lost. Failed to send message: Text: What's up!. Status: Awaiting send | 2024-11-18 03:22:30.647229
Intercepted message: Text: Hi!. Status: Awaiting send
Message successfully delivered: Text: Hi!. Status: Delivered
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: Hi!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: Hi!. Status: Delivered
Message successfully delivered: Text: Hi!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Intercepted message: Text: What's up!. Status: Awaiting send
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Message successfully delivered: Text: Hi!. Status: Delivered
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: Hello!. Status: Delivered
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: What's up!. Status: Delivered
Message successfully delivered: Text: Hi!. Status: Delivered
Message queue for sending: <Queue maxsize=50 _getters[4]>
Message queue for resending: <Queue maxsize=50 _queue=[MessageModel(message='Hi!', status='Awaiting resend'), MessageModel(message="What's up!", status='Awaiting resend')] tasks=2>
```
### Loggers and handlers management in asynchronous code

There are two executing modes for loggers and handlers:

* Fast (default) - coroutines will be wrapped in tasks and executed
* Ordered - coroutines will be executed in specified order

### Fast mode
```python
import asyncio
from datetime import datetime

from intercept_it import UnitInterceptor


async def first_logging_operation() -> None:
    print(f'First handler received logs: {datetime.now()}')
    await asyncio.sleep(5)
    print(f'First handler delivered logs: {datetime.now()}')


async def second_logging_operation() -> None:
    print(f'Second handler received logs: {datetime.now()}')
    await asyncio.sleep(5)
    print(f'Second handler delivered logs: {datetime.now()}')


# Initialize interceptor's object with necessary configuration
interceptor = UnitInterceptor(async_mode=True)

interceptor.register_handler(first_logging_operation)
interceptor.register_handler(second_logging_operation)


@interceptor.intercept(ZeroDivisionError)
async def dangerous_calculation(number: int) -> float:
    return number / 0


if __name__ == '__main__':
    asyncio.run(dangerous_calculation(100))
```
#### Results:
```
First handler received logs: 2024-12-07 13:43:37.524841
Second handler received logs: 2024-12-07 13:43:37.524841
First handler delivered logs: 2024-12-07 13:43:42.532210
Second handler delivered logs: 2024-12-07 13:43:42.532210
```
As you can see, both handlers work together without delay.  

### Ordered mode
```python
# If you want to save execution order in asynchronous code, 
# you can disable handlers wrapping in tasks
interceptor = UnitInterceptor(
    async_mode=True,
    fast_handlers_execution=False 
)

```
#### Results:
```
First handler received logs: 2024-12-07 13:54:29.035445
First handler delivered logs: 2024-12-07 13:54:34.047535
Second handler received logs: 2024-12-07 13:54:34.047535
Second handler delivered logs: 2024-12-07 13:54:39.059667
```
In this case we can see the delay between the execution of handlers.

### Nesting interceptors

If you need to use multiple interceptors with different settings, you can package them in a ``NestedInterceptor``.

This is useful when you can configure everything in a separate module and 
use any of the specified interceptors in any other module

```python
# interceptor_setup.py
from datetime import datetime

from intercept_it import NestedInterceptor, GlobalInterceptor, UnitInterceptor, LoopedInterceptor
from intercept_it.loggers import STDLogger

from intercept_it.utils import cooldown_handler


global_interceptor = GlobalInterceptor(
            exceptions=[ZeroDivisionError, ValueError],
            loggers=[
                STDLogger(default_formatter=lambda message: f"{message} intercepted in global logger {datetime.now()}"),
            ],
        )

global_interceptor.register_handler(
    cooldown_handler,
    5
)

unit_interceptor = UnitInterceptor(
            loggers=[
                STDLogger(default_formatter=lambda message: f"{message} intercepted in unit logger {datetime.now()}")
            ]
        )

unit_interceptor.register_handler(
    cooldown_handler,
    5
)

looped_interceptor = LoopedInterceptor(
            exceptions=[ModuleNotFoundError],
            loggers=[
                STDLogger(default_formatter=lambda message: f"{message} intercepted in looped logger {datetime.now()}")
            ],
            timeout=2
        )

interceptor = NestedInterceptor(
    {
        'Global': global_interceptor,
        8: looped_interceptor,
        IndexError: unit_interceptor,
    }
)
```
You can use any string or integer to specify ``GlobalInterceptor`` and ``LoopedInterceptor`` identifiers.
To specify ``UnitInterceptor`` you need to use exception objects

```python
# main_module.py
import math
from interceptor_setup import interceptor


@interceptor.intercept('Global')
def dangerous_calculation1(some_number: int) -> float:
    return some_number / 0


@interceptor.intercept(IndexError)
def dangerous_list_access(index: int) -> int:
    numbers = [1, 2, 3]
    return numbers[index]


@interceptor.intercept(8)
def dangerous_import() -> None:
    import python


def dangerous_calculation2(some_number: int) -> float:
    return math.sqrt(some_number)


if __name__ == '__main__':
    dangerous_calculation1(5)
    dangerous_list_access(100)

    interceptor.wrap(dangerous_calculation2, 'Global', -1)

    dangerous_import()
```
Note, that you need to specify interceptor identifier in decorators and wrappers.  
This is necessary so that ``NestedInterceptor`` knows which of the interceptors needs to be called

``NestedInterceptor`` can include synchronous and asynchronous interceptors

#### Results:
```
2024-12-07 14:31:47.640265+03:00 | ERROR | division by zero intercepted in global logger 2024-12-07 14:31:47.583100
2024-12-07 14:31:52.644645+03:00 | ERROR | list index out of range intercepted in unit logger 2024-12-07 14:31:52.643645
2024-12-07 14:31:57.645588+03:00 | ERROR | math domain error intercepted in global logger 2024-12-07 14:31:57.645588
2024-12-07 14:32:02.648816+03:00 | ERROR | No module named 'python' intercepted in looped logger 2024-12-07 14:32:02.647814
2024-12-07 14:32:04.651607+03:00 | ERROR | No module named 'python' intercepted in looped logger 2024-12-07 14:32:04.651607
2024-12-07 14:32:06.654012+03:00 | ERROR | No module named 'python' intercepted in looped logger 2024-12-07 14:32:06.654012
2024-12-07 14:32:08.656878+03:00 | ERROR | No module named 'python' intercepted in looped logger 2024-12-07 14:32:08.656878
```
## Future plans

I want to customize exceptions tracing in asynchronous code.  
The following points will allow us to obtain a complete tree of exceptions that occur during the execution of coroutines:

* ExceptionGroup supporting: [PEP-654](https://peps.python.org/pep-0654/)
* Exception notes supporting: [PEP-678](https://peps.python.org/pep-0678/)

I also would like to add additional customization for loggers and add new types of interceptors
