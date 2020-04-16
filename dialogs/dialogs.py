from functools import partial
from typing import Callable, Generator, Any

from .persistence import DialogState


ClientResponse = str
ServerResponse = str

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[[str, "Dialog", DialogState, ClientResponse], DialogGenerator]
Dialog = Callable[[RunSubdialog, DialogState, ClientResponse], DialogGenerator]


def run_dialog(
    dialog: Dialog, state: DialogState, client_response: ClientResponse
) -> DialogGenerator:
    curried_run = partial(_run, client_response=client_response, state=state)

    return dialog(curried_run, state, client_response)


def _run(
    subdialog_id: str,
    subdialog: Dialog,
    state: DialogState,
    client_response: ClientResponse,
):
    subflow_state = state.get_subflow_state(subdialog_id)
    if subflow_state.is_done():
        return subflow_state.get_return_value()

    curried_run = partial(_run, state=subflow_state, client_response=client_response)
    return_value = yield from subdialog(curried_run, subflow_state, client_response)

    subflow_state.set_return_value(return_value)
    return return_value


def prompt(text):
    def _prompt(run: RunSubdialog, state: DialogState, client_response: ClientResponse):
        current_state = state.get_state({"asked": False})
        asked = current_state["asked"]

        if not asked:
            state.save_state({"asked": True})
            yield text

        return client_response

    return _prompt


def chain(dialogs: list):
    def _chain(run: RunSubdialog, state: DialogState, client_response: ClientResponse):
        current_state = state.get_state({"counter": 0, "return_values": []})
        counter = current_state["counter"]
        return_values = current_state["return_values"]

        while counter < len(dialogs):
            dialog = dialogs[counter]

            return_value = yield from run(f"subdialog_{counter}", dialog)

            return_values.append(return_value)
            counter += 1
            state.save_state({"counter": counter, "return_values": return_values})

        return return_values

    return _chain
