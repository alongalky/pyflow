from abc import abstractmethod


class PersistenceProvider:
    @abstractmethod
    def save_state(self, state: dict, outgoing_message):
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass

    @abstractmethod
    def undo(self):
        pass
