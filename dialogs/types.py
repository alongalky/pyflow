from typing import Callable, Generator, Any, List, Union
from dataclasses import dataclass
from abc import abstractmethod


class Dialog:
    @property
    @classmethod
    @abstractmethod
    def version(cls):
        return NotImplementedError

    @abstractmethod
    def __call__(self, run: "RunSubdialog") -> Any:
        pass


class send_to_client:
    version = "1.0"

    def __call__(self):
        raise SendToClientException


@dataclass(frozen=True)
class message:
    text: str
    version = "1.0"

    def __call__(self, send):
        send(self.text)


class SendToClientException(Exception):
    pass


ClientResponse = str
ServerMessage = str
ServerResponse = List[ServerMessage]

AnyDialog = Union[send_to_client, message, Dialog]
DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[[AnyDialog], Any]
