from typing import Tuple

from dialogs import run_dialog, dialog, send_message, get_client_response
from dialogs.persistence.in_memory import InMemoryPersistence


@dialog(version="1.0")
def name_getter_dialog(run) -> str:
    run(send_message("Hello."))
    run(send_message("Nice to meet you!"))
    run(send_message("what is your name?"))
    return run(get_client_response())


@dialog(version="1.1")
def name_getter_dialog_take_2(run) -> str:
    run(send_message("Tell me your name! Now!!!"))
    return run(get_client_response())


@dialog(version="1.0")
def topic_dialog(run) -> Tuple[str, str]:
    name = run(name_getter_dialog)
    run(send_message(f"Hi {name}!"))
    run(send_message("What would you like to talk about"))
    topic = run(get_client_response())
    return name, topic


def test_run_dialog_happy_flow():
    persistence = InMemoryPersistence()

    step1 = run_dialog(name_getter_dialog, persistence, "")
    assert not step1.is_done
    assert len(step1.messages) == 3

    step2 = run_dialog(name_getter_dialog, persistence, "Johnny")
    assert step2.is_done
    assert step2.return_value == "Johnny"


def test_run_dialog_with_subdialog_happy_flow():
    persistence = InMemoryPersistence()
    step1 = run_dialog(topic_dialog, persistence, "")
    assert len(step1.messages) == 3

    step2 = run_dialog(topic_dialog, persistence, "Johnny")
    assert len(step2.messages) == 2
    assert step2.messages[0] == "Hi Johnny!"

    step3 = run_dialog(topic_dialog, persistence, "Peanuts")
    assert step3.is_done
    assert step3.return_value == ("Johnny", "Peanuts")


def test_run_dialog_resets_changed_version():
    persistence = InMemoryPersistence()
    step1 = run_dialog(name_getter_dialog, persistence, "")
    assert len(step1.messages) == 3

    step2 = run_dialog(name_getter_dialog_take_2, persistence, "Johnny")
    assert step2.messages == ["Tell me your name! Now!!!"]

    step3 = run_dialog(name_getter_dialog_take_2, persistence, "Donnie")
    assert step3.is_done
    assert step3.return_value == "Donnie"
