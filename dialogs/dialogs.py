from abc import abstractmethod
from typing import List, Optional

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


class PromptDialog(Dialog):
    def __init__(self, dialog_state: DialogState, prompt: str):
        super().__init__(dialog_state)
        self.dialog_state.set_default_state({"asked": False})
        self.prompt = prompt

    def get_next_message(self, client_response):
        if self.is_done():
            return

        asked = self.dialog_state.get_state()["asked"]

        if not asked:
            self.dialog_state.save_state({"asked": True})
            return self.prompt

        self.dialog_state.set_return_value(client_response)


class DialogChain(Dialog):
    def __init__(self, dialog_state: DialogState, dialogs: List[Dialog]):
        super().__init__(dialog_state)
        self.dialog_state = dialog_state
        self.dialog_state.set_default_state({"counter": 0, "return_values": []})
        self.dialogs = dialogs

    def get_next_message(self, client_response):
        if self.is_done():
            return

        state = self.dialog_state.get_state()
        counter = state["counter"]
        return_values = state["return_values"]

        while counter < len(self.dialogs):
            dialog = self.dialogs[counter]
            response = dialog.get_next_message(client_response)

            if dialog.is_done():
                return_values.append(dialog.get_return_value())

                counter += 1
                self.dialog_state.save_state(
                    {"counter": counter, "return_values": return_values}
                )
            else:
                return response

        self.dialog_state.set_return_value(return_values)
