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
        self.state = {
            "local": "__empty__",
            "subflows": {},
            "is_done": False,
            "return_value": None,
        }
        self.persistence.save_state(self.path, self.state)

    def set_default_state(self, state):
        if self.get_state() == "__empty__":
            self.save_state(state)

    def save_state(self, state):
        self.state = self.persistence.get_state(self.path)
        self.state["local"] = state
        self.persistence.save_state(self.path, self.state)

    def get_state(self):
        return self.persistence.get_state(self.path)["local"]

    def get_subflow_dialog_state(self, subflow_id: str):
        return DialogState(
            persistence=self.persistence, path=[*self.path, "subflows", subflow_id]
        )

    def set_return_value(self, return_value):
        self.state = self.persistence.get_state(self.path)
        if self.state["is_done"]:
            raise Exception("Dialog is done, cannot set return value")

        self.state["return_value"] = return_value
        self.state["is_done"] = True
        self.persistence.save_state(self.path, self.state)

    def get_return_value(self) -> object:
        self.state = self.persistence.get_state(self.path)
        if not self.state["is_done"]:
            raise StopIteration("Dialog not done yet")

        return self.state["return_value"]

    def is_done(self) -> bool:
        return self.persistence.get_state(self.path)["is_done"]
