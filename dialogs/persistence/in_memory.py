from dataclasses import dataclass, field

from .persistence import PersistenceProvider


@dataclass
class InMemoryPersistence(PersistenceProvider):
    state: dict = field(default_factory=dict)

    def save_state(self, path, state):
        if path:
            sub_state = self.state

            for key in path[:-1]:
                sub_state = sub_state.setdefault(key, {})
            sub_state[path[-1]] = state
        else:
            self.state = state

    def get_state(self, path):
        sub_state = self.state

        for k in path:
            sub_state = sub_state[k]

        return sub_state
