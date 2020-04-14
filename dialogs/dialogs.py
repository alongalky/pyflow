from abc import abstractmethod
from typing import Optional

from .persistence import DialogState


ClientResponse = str
ServerResponse = str


class Dialog:
    def __init__(self, dialog_state: DialogState):
        self.dialog_state = dialog_state

    def get_return_value(self) -> object:
        return self.dialog_state.get_return_value()

    def is_done(self) -> bool:
        return self.dialog_state.is_done()

    @abstractmethod
    def get_next_message(self, client_response) -> Optional[ServerResponse]:
        pass


def prompt(text):
    def _prompt(state: DialogState, client_response: ClientResponse):
        if state.is_done():
            return state.get_return_value()

        state.set_default_state({"asked": False})
        asked = state.get_state()["asked"]

        if not asked:
            state.save_state({"asked": True})
            yield text

        state.set_return_value(client_response)
        return client_response

    return _prompt


def chain(dialogs: list):
    def _chain(state: DialogState, client_response: ClientResponse):
        if state.is_done():
            return state.get_return_value()

        state.set_default_state({"counter": 0, "return_values": []})

        current_state = state.get_state()
        counter = current_state["counter"]
        return_values = current_state["return_values"]

        while counter < len(dialogs):
            subflow_state = state.subflow(f"subdialog_{counter}")
            dialog = dialogs[counter]

            return_value = yield from dialog(subflow_state, client_response)

            return_values.append(return_value)
            counter += 1
            state.save_state({"counter": counter, "return_values": return_values})

        return return_values

    return _chain
