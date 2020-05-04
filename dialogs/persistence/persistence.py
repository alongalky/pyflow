from abc import abstractmethod

from ..types import PrimitiveOrDialog


class PersistenceProvider:
    @abstractmethod
    def save_state(self, state: dict):
        pass

    @abstractmethod
    def get_state(self, dialog: PrimitiveOrDialog) -> dict:
        pass
