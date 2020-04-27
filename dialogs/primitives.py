from typing import List, Any

from .types import (
    Dialog,
    DialogGenerator,
    ClientResponse,
    RunSubdialog,
    message,
    send_to_client,
)


def prompt(text) -> Dialog:
    def _prompt(run: RunSubdialog) -> ClientResponse:
        run(message(text))
        return run(send_to_client())

    return _prompt


def chain(dialogs: list) -> Dialog:
    def _chain(run: RunSubdialog) -> List[Any]:
        return [run(dialog) for dialog in dialogs]

    return _chain


def multichoice(question: str, wrong_answer_prompt: str, choices: List[str]) -> Dialog:
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


def yes_no(question: str, wrong_answer_prompt: str) -> Dialog:
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
