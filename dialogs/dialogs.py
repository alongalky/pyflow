from functools import partial
from itertools import count
from typing import Iterator

from .types import Dialog, DialogGenerator, ClientResponse, SendToClientException
from .persistence import DialogState
from .primitives import send_to_client, message
from .message_queue import MessageQueue


def run_dialog(
    dialog: Dialog, state: DialogState, client_response: ClientResponse
) -> DialogGenerator:
    queue = MessageQueue()
    send = queue.enqueue

    try:
        return _run(dialog, state, client_response, send, count())
    except SendToClientException:
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

    if isinstance(subdialog, send_to_client):
        if not subflow_state.sent_to_client():
            subflow_state.set_sent_to_client()
            return subdialog()
        else:
            return_value = client_response
    elif isinstance(subdialog, message):
        return_value = subdialog(send)
    else:
        curried_run = partial(
            _run,
            state=subflow_state,
            client_response=client_response,
            send=send,
            call_counter=count(),
        )
        return_value = subdialog(curried_run)

    subflow_state.set_return_value(return_value)
    return return_value
