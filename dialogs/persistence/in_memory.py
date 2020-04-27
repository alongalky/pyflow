from dataclasses import dataclass, field
import copy

from .persistence import PersistenceProvider
from dialogs.dialog_state import new_empty_state


@dataclass
class InMemoryPersistence(PersistenceProvider):
    history: list = field(default_factory=lambda: [new_empty_state()])
    outgoing_messages: list = field(default_factory=list)

    def save_state(self, state, outgoing_message):
        self.history.append(copy.deepcopy(state))
        self.outgoing_messages.append(outgoing_message)

    def get_state(self):
        return copy.deepcopy(self.history[-1]) if self.history else new_empty_state()

    def undo(self):
        if len(self.history) > 2:
            self.history.pop()
            self.outgoing_messages.pop()
        return self.outgoing_messages[-1]
