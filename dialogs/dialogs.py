from functools import partial

from .types import Dialog, DialogGenerator, ClientResponse, RunSubdialog, DialogState


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
