from typing import List

from .types import Dialog, DialogGenerator, ClientResponse, RunSubdialog, DialogState


def prompt(text) -> Dialog:
    def _prompt(
        run: RunSubdialog, state: DialogState, client_response: ClientResponse
    ) -> DialogGenerator:
        current_state = state.get_state({"asked": False})
        asked = current_state["asked"]

        if not asked:
            state.save_state({"asked": True})
            yield text

        return client_response

    return _prompt


def chain(dialogs: list) -> Dialog:
    def _chain(
        run: RunSubdialog, state: DialogState, client_response: ClientResponse
    ) -> DialogGenerator:
        current_state = state.get_state({"counter": 0, "return_values": []})
        counter = current_state["counter"]
        return_values = current_state["return_values"]

        while counter < len(dialogs):
            dialog = dialogs[counter]

            return_value = yield from run(f"subdialog_{counter}", dialog)

            return_values.append(return_value)
            counter += 1
            state.save_state({"counter": counter, "return_values": return_values})

        return return_values

    return _chain


def multichoice(question: str, wrong_answer_prompt: str, choices: List[str]) -> Dialog:
    def _multichoice(
        run: RunSubdialog, state: DialogState, client_response: ClientResponse
    ) -> DialogGenerator:
        current_state = state.get_state({"counter": 0})
        counter = current_state["counter"]

        while True:
            message = question if counter == 0 else wrong_answer_prompt
            text = "\n".join(
                [message] + [f"{i+1}. {choice}" for i, choice in enumerate(choices)]
            )
            answer = yield from run(f"attempt_{counter}", prompt(text))

            valid_answers = {str(i + 1) for i in range(len(choices))}
            if answer in valid_answers:
                break

            counter += 1
            state.save_state({"counter": counter})

        return int(answer) - 1

    return _multichoice
