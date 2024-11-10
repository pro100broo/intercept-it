from enum import Enum


class WarningLevelsEnum(Enum):
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class TimeCooldownsEnum(Enum):
    FIVE_MINUTES = 300
    ONE_MINUTE = 60
    FIVE_SECONDS = 5
    ZERO = 0


class ResumeFlagsEnum(Enum):
    CONTINUE_EXECUTION = 'CONTINUE_EXECUTION'
    STOP_EXECUTION = 'STOP_EXECUTION'
