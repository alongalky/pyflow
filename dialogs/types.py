from typing import Callable, Generator, Any

from .persistence import DialogState


ClientResponse = str
ServerResponse = str

DialogGenerator = Generator[ServerResponse, None, Any]
RunSubdialog = Callable[[str, "Dialog", DialogState, ClientResponse], DialogGenerator]
Dialog = Callable[[RunSubdialog, DialogState, ClientResponse], DialogGenerator]
