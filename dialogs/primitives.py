from typing import List, Any

from .types import (
    PrimitiveOrDialog,
    Dialog,
    ClientResponse,
    RunSubdialog,
    message,
    send_to_client,
    dialog,
)


def prompt(text):
    @dialog(version="1.0")
    def _prompt(run: RunSubdialog) -> ClientResponse:
        run(message(text))
        return run(send_to_client())

    return _prompt


def chain(dialogs: List[PrimitiveOrDialog]) -> Dialog:
    @dialog(version="1.0")
    def _chain(run: RunSubdialog) -> List[Any]:
        return [run(dialog) for dialog in dialogs]

    return _chain


def multichoice(question: str, wrong_answer_prompt: str, choices: List[str]):
    @dialog(version="1.0")
    def _multichoice(run: RunSubdialog) -> int:
        first_time = True

        while True:
            message = question if first_time else wrong_answer_prompt
            text = "\n".join(
                [message] + [f"{i+1}. {choice}" for i, choice in enumerate(choices)]
            )
            answer = run(prompt(text))

            valid_answers = {str(i + 1) for i in range(len(choices))}
            if answer in valid_answers:
                return int(answer) - 1

            first_time = False

    return _multichoice


def yes_no(question: str, wrong_answer_prompt: str):
    @dialog(version="1.0")
    def _yes_no(run: RunSubdialog) -> bool:
        first_time = True

        while True:
            message = question if first_time else wrong_answer_prompt
            answer = run(prompt(message)).strip().lower()

            valid_answer_values = {"n": False, "no": False, "y": True, "yes": True}
            if answer in valid_answer_values:
                return valid_answer_values[answer]

            first_time = False

    return _yes_no
