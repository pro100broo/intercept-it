from abc import ABC, abstractmethod


class BaseLogger(ABC):

    @staticmethod
    @abstractmethod
    def save_logs(message: str) -> None:
        pass
