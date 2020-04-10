from abc import abstractmethod
from dataclasses import dataclass
from typing import Union, List

from .persistence import DialogState


@dataclass(frozen=True)
class Done:
    return_value: object


@dataclass(frozen=True)
class ServerResponse:
    response: str


class Dialog:
    @abstractmethod
    def get_next_message(self, client_response) -> Union[ServerResponse, Done]:
        pass


class PromptDialog(Dialog):
    def __init__(self, dialog_state: DialogState, prompt: str):
        self.dialog_state = dialog_state
        self.dialog_state.set_default_state({"asked": False})
        self.prompt = prompt

    def get_next_message(self, client_response):
        asked = self.dialog_state.get_state()["asked"]

        if asked:
            response = Done(return_value=client_response)
        else:
            response = ServerResponse(response=self.prompt)

        self.dialog_state.save_state({"asked": True})

        return response


class DialogChain(Dialog):
    def __init__(self, dialog_state: DialogState, dialogs: List[Dialog]):
        self.dialog_state = dialog_state
        self.dialog_state.set_default_state({"counter": 0, "return_values": []})
        self.dialogs = dialogs

    def get_next_message(self, client_response):
        state = self.dialog_state.get_state()
        counter = state["counter"]
        return_values = state["return_values"]

        while True:
            if counter == len(self.dialogs):
                return Done(return_value=return_values)

            response = self.dialogs[counter].get_next_message(client_response)
            if isinstance(response, Done):
                return_values.append(response.return_value)
                counter += 1
                self.dialog_state.save_state(
                    {"counter": counter, "return_values": return_values}
                )
            else:
                return response

        return response
