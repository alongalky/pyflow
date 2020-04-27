from dataclasses import dataclass, field
from typing import List

from .types import ServerMessage


@dataclass
class MessageQueue:
    _queue: List[ServerMessage] = field(default_factory=list)

    def enqueue(self, message: ServerMessage):
        self._queue.append(message)

    def dequeue_all(self) -> List[ServerMessage]:
        messages = self._queue
        self._queue = []
        return messages
