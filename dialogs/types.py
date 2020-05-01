from typing import Callable, Any, List, Union
from typing_extensions import Protocol
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Dialog:
    dialog: "DialogFunction"
    version: str
    name: str


class get_client_response:
    version = "1.0"
    name = "get_client_response"

    def __call__(self):
        raise SendToClientException


@dataclass(frozen=True)
class send_message:
    text: str
    version = "1.0"
    name = "send_message"

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

PrimitiveOrDialog = Union[get_client_response, send_message, Dialog]
RunSubdialog = Callable[[PrimitiveOrDialog], Any]


@dataclass(frozen=True)
class DialogStep:
    is_done: bool = False
    return_value: Any = None
    messages: List[ServerMessage] = field(default_factory=list)
