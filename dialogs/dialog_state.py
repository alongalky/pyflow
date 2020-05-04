from dataclasses import dataclass

from .types import PrimitiveOrDialog, get_client_response


def new_empty_state(dialog: PrimitiveOrDialog):
    empty_state = {
        "subdialogs": [],
        "is_done": False,
        "return_value": None,
        "version": dialog.version,
        "name": dialog.name,
    }

    if isinstance(dialog, get_client_response):
        empty_state["sent_to_client"] = False

    return empty_state


@dataclass(frozen=True)
class DialogState:
    state: dict

    def get_subdialog_state(self, subdialog_index: int, subdialog: PrimitiveOrDialog):
        if len(self.state["subdialogs"]) == subdialog_index:
            self.state["subdialogs"].append(new_empty_state(subdialog))

        subdialog_state = DialogState(self.state["subdialogs"][subdialog_index])
        if subdialog_state.version != subdialog.version:
            subdialog_state.reset(subdialog)

        return subdialog_state

    def sent_to_client(self):
        return self.state.get("sent_to_client", False)

    def set_sent_to_client(self):
        self.state["sent_to_client"] = True

    def set_return_value(self, return_value):
        if self.state["is_done"]:
            raise Exception("Dialog is done, cannot set return value")

        self.state["return_value"] = return_value
        self.state["is_done"] = True

    def get_return_value(self) -> object:
        if not self.state["is_done"]:
            raise Exception("Dialog not done yet")

        return self.state["return_value"]

    def is_done(self) -> bool:
        return self.state["is_done"]

    @property
    def version(self):
        return self.state["version"]

    def reset(self, dialog: PrimitiveOrDialog):
        self.state.pop("sent_to_client", None)
        self.state.update(new_empty_state(dialog))
