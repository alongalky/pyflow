from functools import partial
from itertools import count
from typing import Iterator

from .types import (
    Dialog,
    PrimitiveOrDialog,
    DialogGenerator,
    ClientResponse,
    SendToClientException,
    send_to_client,
    message,
)
from .persistence import PersistenceProvider
from .dialog_state import DialogState
from .message_queue import MessageQueue


def run_dialog(
    dialog: PrimitiveOrDialog,
    persistence: PersistenceProvider,
    client_response: ClientResponse,
) -> DialogGenerator:
    if client_response == "undo":
        yield persistence.undo()

    queue = MessageQueue()
    send = queue.enqueue

    state = persistence.get_state(dialog)

    try:
        return _run(dialog, DialogState(state), client_response, send, count())
    except SendToClientException:
        messages = queue.dequeue_all()
        persistence.save_state(state, messages)
        yield messages


def _run(
    subdialog: PrimitiveOrDialog,
    state: DialogState,
    client_response: ClientResponse,
    send,
    call_counter: Iterator[int],
):
    subdialog_state = state.get_subdialog_state(next(call_counter), subdialog)
    if subdialog_state.is_done():
        return subdialog_state.get_return_value()

    if isinstance(subdialog, send_to_client):
        if not subdialog_state.sent_to_client():
            subdialog_state.set_sent_to_client()
            return subdialog()
        else:
            return_value = client_response
    elif isinstance(subdialog, message):
        return_value = subdialog(send)
    elif isinstance(subdialog, Dialog):
        curried_run = partial(
            _run,
            state=subdialog_state,
            client_response=client_response,
            send=send,
            call_counter=count(),
        )
        return_value = subdialog.dialog(curried_run)
    else:
        raise Exception("Unsupported dialog type")

    subdialog_state.set_return_value(return_value)
    return return_value
