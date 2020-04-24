from functools import partial
from itertools import count
from typing import Iterator

from .types import Dialog, DialogGenerator, ClientResponse, DialogState
from .persistence import PersistenceProvider


def run_dialog(
    dialog: Dialog, persistence: PersistenceProvider, client_response: ClientResponse
) -> DialogGenerator:
    if client_response == "undo":
        yield persistence.undo()

    state = persistence.get_state()

    curried_run = partial(
        _run,
        client_response=client_response,
        state=DialogState(state),
        call_counter=count(),
    )

    for message in dialog(curried_run, DialogState(state), client_response):
        persistence.save_state(state, message)
        yield message


def _run(
    subdialog: Dialog,
    state: DialogState,
    client_response: ClientResponse,
    call_counter: Iterator[int],
):
    call_count = next(call_counter)
    subdialog_id = f"subdialog_{call_count}"
    subflow_state = state.get_subflow_state(subdialog_id)
    if subflow_state.is_done():
        return subflow_state.get_return_value()

    curried_run = partial(
        _run, state=subflow_state, client_response=client_response, call_counter=count()
    )
    return_value = yield from subdialog(curried_run, subflow_state, client_response)

    subflow_state.set_return_value(return_value)
    return return_value
