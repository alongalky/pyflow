from .types import Dialog, DialogGenerator, ClientResponse, RunSubdialog, DialogState


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
