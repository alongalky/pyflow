from functools import partial
from itertools import count
from typing import Iterator

from .types import Dialog, DialogGenerator, ClientResponse, DialogState
from .message_queue import MessageQueue


def run_dialog(
    dialog: Dialog, state: DialogState, client_response: ClientResponse
) -> DialogGenerator:
    queue = MessageQueue()
    send = queue.enqueue

    curried_run = partial(
        _run,
        client_response=client_response,
        state=state,
        send=send,
        call_counter=count(),
    )

    for _ in dialog(curried_run, state, client_response, send):
        yield queue.dequeue_all()


def _run(
    subdialog: Dialog,
    state: DialogState,
    client_response: ClientResponse,
    send,
    call_counter: Iterator[int],
):
    call_count = next(call_counter)
    subdialog_id = f"subdialog_{call_count}"
    subflow_state = state.get_subflow_state(subdialog_id)
    if subflow_state.is_done():
        return subflow_state.get_return_value()

    curried_run = partial(_run, subflow_state, client_response, send, count())
    return_value = yield from subdialog(
        curried_run, subflow_state, client_response, send
    )

    subflow_state.set_return_value(return_value)
    return return_value
