from abc import abstractmethod

from dialogs.types import PrimitiveOrDialog


class PersistenceProvider:
    @abstractmethod
    def save_state(self, state: dict, outgoing_message):
        pass

    @abstractmethod
    def get_state(self, dialog: PrimitiveOrDialog) -> dict:
        pass

    @abstractmethod
    def undo(self):
        pass
