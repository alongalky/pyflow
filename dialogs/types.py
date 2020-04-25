from typing import Callable, Generator, Any
from dataclasses import dataclass

from .persistence import DialogState


ClientResponse = str
ServerResponse = str

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[["Dialog"], Any]
Dialog = Callable[[RunSubdialog, DialogState, ClientResponse], Any]


@dataclass(frozen=True)
class SendToClientException(Exception):
    message: ServerResponse
