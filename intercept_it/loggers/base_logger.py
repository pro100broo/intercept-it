from abc import ABC, abstractmethod


class BaseLogger(ABC):
    """ Logger interface """
    @staticmethod
    @abstractmethod
    def save_logs(message: str) -> None:
        pass
