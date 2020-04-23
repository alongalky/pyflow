from dataclasses import dataclass, field

from .persistence import PersistenceProvider


@dataclass
class InMemoryPersistence(PersistenceProvider):
    state: dict = field(default_factory=dict)
    outgoing_message_queue: list = field(default_factory=list)

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
            if k not in sub_state:
                return None
            sub_state = sub_state[k]

        return sub_state

    def enqueue(self, message):
        self.outgoing_message_queue.append(message)

    def dequeue_all(self) -> list:
        messages = self.outgoing_message_queue
        self.outgoing_message_queue = []
        return messages
