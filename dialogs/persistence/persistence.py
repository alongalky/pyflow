from dataclasses import dataclass, field
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


def new_empty_state():
    return {
        "local": "__empty__",
        "subflows": {},
        "is_done": False,
        "return_value": None,
    }


@dataclass(frozen=True)
class DialogState:
    state: dict = field(default_factory=new_empty_state)

    def save_state(self, state):
        self.state["local"] = state

    def get_state(self, default_state):
        self._set_default_state(default_state)

        return self.state["local"]

    def get_subflow_state(self, subflow_id: str):
        if subflow_id not in self.state["subflows"]:
            self.state["subflows"][subflow_id] = new_empty_state()

        return DialogState(state=self.state["subflows"][subflow_id])

    def _set_default_state(self, state):
        if self.state["local"] == "__empty__":
            self.save_state(state)

    def set_return_value(self, return_value):
        if self.state["is_done"]:
            raise Exception("Dialog is done, cannot set return value")

        self.state["return_value"] = return_value
        self.state["is_done"] = True

    def get_return_value(self) -> object:
        if not self.state["is_done"]:
            raise StopIteration("Dialog not done yet")

        return self.state["return_value"]

    def is_done(self) -> bool:
        return self.state["is_done"]
