from typing import Callable, Generator, Any, List, Union
from typing_extensions import Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class Dialog:
    dialog: "DialogFunction"
    version: str
    name: str


class send_to_client:
    version = "1.0"
    name = "send_to_client"

    def __call__(self):
        raise SendToClientException


@dataclass(frozen=True)
class message:
    text: str
    version = "1.0"
    name = "message"

    def __call__(self, send):
        send(self.text)


class SendToClientException(Exception):
    pass


def dialog(version: str):
    def _dialog(f):
        return Dialog(version=version, name=f.__name__, dialog=f)

    return _dialog


class DialogFunction(Protocol):
    def __call__(self, run: "RunSubdialog") -> Any:
        ...


ClientResponse = str
ServerMessage = str
ServerResponse = List[ServerMessage]

PrimitiveOrDialog = Union[send_to_client, message, Dialog]
DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[[PrimitiveOrDialog], Any]
