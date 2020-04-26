from typing import Callable, Generator, Any, List, Union
from dataclasses import dataclass


class send_to_client:
    def __call__(self):
        raise SendToClientException


@dataclass(frozen=True)
class message:
    text: str

    def __call__(self, send):
        send(self.text)


class SendToClientException(Exception):
    pass


ClientResponse = str
ServerMessage = str
ServerResponse = List[ServerMessage]

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[["Dialog"], Any]
SendMessage = Callable[[ServerMessage], None]
CompoundDialog = Callable[[RunSubdialog], Any]
Dialog = Union[CompoundDialog, send_to_client, message]
