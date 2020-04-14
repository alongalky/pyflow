from functools import partial

from .persistence import DialogState


ClientResponse = str
ServerResponse = str


def run(
    subflow_id: str, subflow: callable, state: DialogState, response: ClientResponse
):
    subflow_state = state.get_subflow_state(subflow_id)
    if subflow_state.is_done():
        return subflow_state.get_return_value()

    return_value = yield from subflow(
        partial(run, state=subflow_state, response=response), subflow_state, response
    )

    subflow_state.set_return_value(return_value)
    return return_value


def prompt(text):
    def _prompt(run, state: DialogState, client_response: ClientResponse):
        current_state = state.get_state({"asked": False})
        asked = current_state["asked"]

        if not asked:
            state.save_state({"asked": True})
            yield text

        return client_response

    return _prompt


def chain(dialogs: list):
    def _chain(run, state: DialogState, client_response: ClientResponse):
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
