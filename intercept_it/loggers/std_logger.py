import sys
import pytz

from datetime import datetime
from loguru import logger
from typing import Callable

from intercept_it.utils.enums import WarningLevelsEnum
from intercept_it.utils.default_formatters import std_formatter
from intercept_it.loggers.base_logger import BaseLogger


class STDLogger(BaseLogger):
    """Implements saving logs to the text file"""

    def __init__(
            self,
            logging_level: str = WarningLevelsEnum.ERROR.value,
            pytz_timezone: str = 'Europe/Moscow',
            default_formatter: Callable = std_formatter
    ):
        self._logger = logger
        self._logging_level = logging_level
        self._default_timezone = pytz_timezone
        self._message_formatter = default_formatter

        self._logger.configure(
            handlers=[
                {
                    'sink': sys.stdout,
                    'format': '{extra[datetime]} | {level} | {message}',
                },
            ],
            patcher=self._patch_timezone
        )

    def _patch_timezone(self, record):
        record['extra']['datetime'] = datetime.now(tz=pytz.timezone(self._default_timezone))

    def save_logs(self, message: str) -> None:
        message = self._message_formatter(message)
        if self._logging_level == WarningLevelsEnum.INFO.value:
            self._logger.info(message)
        if self._logging_level == WarningLevelsEnum.ERROR.value:
            self._logger.error(message)
        if self._logging_level == WarningLevelsEnum.WARNING.value:
            self._logger.warning(message)

