from typing import Callable, Generator, Any, List
from dataclasses import dataclass
from abc import abstractmethod


class Dialog:
    @property
    @classmethod
    @abstractmethod
    def version(cls):
        return NotImplementedError


class send_to_client(Dialog):
    version = "1.0"

    def __call__(self):
        raise SendToClientException


@dataclass(frozen=True)
class message(Dialog):
    text: str
    version = "1.0"

    def __call__(self, send):
        send(self.text)


class SendToClientException(Exception):
    pass


ClientResponse = str
ServerMessage = str
ServerResponse = List[ServerMessage]

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[[Dialog], Any]
