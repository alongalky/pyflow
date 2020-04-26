from typing import Callable, Generator, Any, List

from .persistence import DialogState


ClientResponse = str
ServerMessage = str
ServerResponse = List[ServerMessage]

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[["Dialog"], DialogGenerator]
SendMessage = Callable[[ServerMessage], None]
Dialog = Callable[
    [RunSubdialog, DialogState, ClientResponse, SendMessage], DialogGenerator
]
