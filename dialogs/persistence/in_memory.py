from dataclasses import dataclass, field
import copy

from .persistence import PersistenceProvider
from ..dialog_state import new_empty_state
from ..types import PrimitiveOrDialog


@dataclass
class InMemoryPersistence(PersistenceProvider):
    state: dict = field(default_factory=dict)

    def save_state(self, state):
        self.state = copy.deepcopy(state)

    def get_state(self, dialog: PrimitiveOrDialog):
        return copy.deepcopy(self.state) if self.state else new_empty_state(dialog)
