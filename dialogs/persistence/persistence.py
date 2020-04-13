from dataclasses import dataclass, field
from abc import abstractmethod
from typing import List
import copy


class PersistenceProvider:
    @abstractmethod
    def save_state(self, path: List[str], state: dict):
        pass

    def get_state(self, path: List[str]) -> dict:
        pass


EMPTY_STATE = {
    "local": "__empty__",
    "subflows": {},
    "is_done": False,
    "return_value": None,
}


@dataclass(frozen=True)
class DialogState:
    persistence: PersistenceProvider
    path: List[str] = field(default_factory=list)

    def set_default_state(self, state):
        if self.get_state() == "__empty__":
            self.save_state(state)

    def save_state(self, state):
        previous_state = self._get_full_state()
        new_state = {**previous_state, "local": state}
        self.persistence.save_state(self.path, new_state)

    def get_state(self):
        return self._get_full_state()["local"]

    def _get_full_state(self):
        state = self.persistence.get_state(self.path)
        if not state:
            new_empty_state = copy.deepcopy(EMPTY_STATE)
            self.persistence.save_state(self.path, new_empty_state)
            state = EMPTY_STATE
        return state

    def subflow_state(self, subflow_id: str):
        return DialogState(
            persistence=self.persistence, path=[*self.path, "subflows", subflow_id]
        )

    def set_return_value(self, return_value):
        state = self._get_full_state()
        if state["is_done"]:
            raise Exception("Dialog is done, cannot set return value")

        state["return_value"] = return_value
        state["is_done"] = True
        self.persistence.save_state(self.path, state)

    def get_return_value(self) -> object:
        state = self.persistence.get_state(self.path)
        if not state["is_done"]:
            raise StopIteration("Dialog not done yet")

        return state["return_value"]

    def is_done(self) -> bool:
        return self._get_full_state()["is_done"]
