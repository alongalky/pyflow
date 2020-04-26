from functools import partial
from itertools import count
from typing import Iterator

from .types import Dialog, DialogGenerator, ClientResponse, DialogState


def run_dialog(
    dialog: Dialog, state: DialogState) -> DialogGenerator:
    curried_run = partial(
        _run, state=state, call_counter=count()
    )

    return dialog(curried_run, state)


def _run(
    subdialog: Dialog,
    state: DialogState,
    call_counter: Iterator[int],
):
    call_count = next(call_counter)
    subdialog_id = f"subdialog_{call_count}"
    subflow_state = state.get_subflow_state(subdialog_id)
    if subflow_state.is_done():
        return subflow_state.get_return_value()

    curried_run = partial(
        _run, state=subflow_state, call_counter=count()
    )
    return_value = yield from subdialog(curried_run, subflow_state)

    subflow_state.set_return_value(return_value)
    return return_value
