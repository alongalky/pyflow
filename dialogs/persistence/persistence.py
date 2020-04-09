from abc import abstractmethod
from typing import List


class PersistenceProvider:
    @abstractmethod
    def save_state(self, path: List[str], state: dict):
        pass

    def get_state(self, path: List[str]) -> dict:
        pass


class DialogState:
    def __init__(self, persistence: PersistenceProvider, path: List[str] = []):
        self.persistence = persistence
        self.path = path
        self.state = {"local": "__empty__", "subflows": {}}
        self.persistence.save_state(self.path, self.state)

    def set_default_state(self, state):
        if self.get_state() == "__empty__":
            self.save_state(state)

    def save_state(self, state):
        self.state["local"] = state
        self.persistence.save_state(self.path, self.state)

    def get_state(self):
        return self.persistence.get_state(self.path)["local"]

    def get_subflow_dialog_state(self, subflow_id: str):
        return DialogState(
            persistence=self.persistence, path=[*self.path, "subflows", subflow_id]
        )
