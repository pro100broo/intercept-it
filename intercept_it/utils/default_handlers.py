import time

from intercept_it.utils import ResumeFlagsEnum
from intercept_it.exceptions import ContinueProgramException, StopProgramException


def cooldown_handler(waiting_time_in_seconds: int) -> None:
    """
    Select time dilation after exception handling. Program will sleep at the specified time

    :param waiting_time_in_seconds: Time dilation value in seconds
    """
    time.sleep(waiting_time_in_seconds)


def resuming_handler(flag: str) -> None:
    """
    Select how the program will react to a specific exception according to flag:

    * CONTINUE_EXECUTION -> Continue program execution after handling exception
    * STOP_EXECUTION -> Stop program execution after handling exception

    :param flag: Exception handling logic
    :raise ContinueProgramException: If flag param is equal ``RESUME_PROGRAM``
    :raise StopProgramException: If flag param is equal ``STOP_PROGRAM``
    """
    match flag:
        case ResumeFlagsEnum.CONTINUE_EXECUTION.value:
            raise ContinueProgramException
        case ResumeFlagsEnum.STOP_EXECUTION.value:
            raise StopProgramException
