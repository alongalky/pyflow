from dialogs import dialog
from dialogs.persistence.in_memory import InMemoryPersistence
from dialogs.dialog_state import new_empty_state


@dialog(version="1.0")
def some_dialog():
    return 6


def test_save_state_get_state_happy_flow():
    persistence = InMemoryPersistence()
    persistence.save_state({"nice": "state"})

    assert persistence.get_state(some_dialog) == {"nice": "state"}


def test_get_empty_state():
    persistence = InMemoryPersistence()

    assert persistence.get_state(some_dialog) == new_empty_state(some_dialog)
