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
    return {"subdialogs": [], "is_done": False, "return_value": None}


@dataclass(frozen=True)
class DialogState:
    state: dict = field(default_factory=new_empty_state)

    def get_subdialog_state(self, subdialog_index: int):
        if len(self.state["subdialogs"]) == subdialog_index:
            self.state["subdialogs"].append(new_empty_state())

        return DialogState(state=self.state["subdialogs"][subdialog_index])

    def sent_to_client(self):
        return "sent_to_client" in self.state

    def set_sent_to_client(self):
        self.state["sent_to_client"] = True

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
