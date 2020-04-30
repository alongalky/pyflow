from typing import List, Any
from dataclasses import dataclass

from .types import (
    PrimitiveOrDialog,
    Dialog,
    ClientResponse,
    RunSubdialog,
    message,
    send_to_client,
)


@dataclass(frozen=True)
class prompt(Dialog):
    text: str
    version = "1.0"

    def __call__(self, run: RunSubdialog) -> ClientResponse:
        run(message(self.text))
        return run(send_to_client())


@dataclass(frozen=True)
class chain(Dialog):
    dialogs: List[PrimitiveOrDialog]
    version = "1.0"

    def __call__(self, run: RunSubdialog) -> List[Any]:
        return [run(dialog) for dialog in self.dialogs]


@dataclass(frozen=True)
class multichoice(Dialog):
    question: str
    wrong_answer_prompt: str
    choices: List[str]
    version = "1.0"

    def __call__(self, run: RunSubdialog) -> int:
        first_time = True

        while True:
            message = self.question if first_time else self.wrong_answer_prompt
            text = "\n".join(
                [message]
                + [f"{i+1}. {choice}" for i, choice in enumerate(self.choices)]
            )
            answer = run(prompt(text))

            valid_answers = {str(i + 1) for i in range(len(self.choices))}
            if answer in valid_answers:
                return int(answer) - 1

            first_time = False


@dataclass(frozen=True)
class yes_no(Dialog):
    question: str
    wrong_answer_prompt: str
    version = "1.0"

    def __call__(self, run: RunSubdialog) -> bool:
        first_time = True

        while True:
            message = self.question if first_time else self.wrong_answer_prompt
            answer = run(prompt(message)).strip().lower()

            valid_answer_values = {"n": False, "no": False, "y": True, "yes": True}
            if answer in valid_answer_values:
                return valid_answer_values[answer]

            first_time = False
