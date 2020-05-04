import pytest

from ..dialogs.types import get_client_response, send_message, dialog
from ..dialogs.dialog_state import DialogState, new_empty_state


@dialog(version="1.0")
def fun_dialog(run):
    run(send_message("Hi there."))
    run(send_message("How are you?"))
    return run(get_client_response())


def test_new_empty_state_correct_for_get_client_response():
    state = new_empty_state(get_client_response())

    assert state == {
        "subdialogs": [],
        "is_done": False,
        "return_value": None,
        "version": "1.0",
        "name": "get_client_response",
        "sent_to_client": False,
    }


def test_new_empty_state_correct_for_send_message():
    state = new_empty_state(send_message("some message"))

    assert state == {
        "subdialogs": [],
        "is_done": False,
        "return_value": None,
        "version": "1.0",
        "name": "send_message",
    }


def test_new_empty_state_correct_for_dialog():
    state = new_empty_state(fun_dialog)

    assert state == {
        "subdialogs": [],
        "is_done": False,
        "return_value": None,
        "version": "1.0",
        "name": "fun_dialog",
    }


def test_get_subdialog_state_new_state_case():
    state = DialogState(new_empty_state(fun_dialog))
    subdialog_state = state.get_subdialog_state(0, send_message("Hi!"))

    assert not subdialog_state.is_done()


def test_get_subdialog_state_refetch_existing_subdialog_state():
    state = DialogState(new_empty_state(fun_dialog))
    subdialog_state = state.get_subdialog_state(0, send_message("Hi!"))
    subdialog_state.set_return_value(6)

    # Now fetch the state again, and see that the return value is retained
    subdialog_state_second_fetch = state.get_subdialog_state(0, send_message("Hi!"))
    assert subdialog_state_second_fetch.is_done()
    assert subdialog_state_second_fetch.get_return_value() == 6


def test_set_return_value_sets_is_done():
    state = DialogState(new_empty_state(fun_dialog))

    state.set_return_value(6)

    assert state.get_return_value() == 6
    assert state.is_done()


def test_set_return_value_twice_raises_exception():
    state = DialogState(new_empty_state(fun_dialog))
    state.set_return_value(6)

    with pytest.raises(Exception):
        state.set_return_value(6)


def test_get_return_value_before_set_raises_exception():
    state = DialogState(new_empty_state(fun_dialog))

    with pytest.raises(Exception):
        state.get_return_value()


def test_version_property():
    @dialog(version="123")
    def some_dialog(run):
        pass

    state = DialogState(new_empty_state(some_dialog))

    assert state.version == "123"
