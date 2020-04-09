from dataclasses import dataclass

from dialogs.persistence import InMemoryPersistence, DialogState
from dialogs import PromptDialog, ServerResponse, Dialog, Done, DialogChain


class IntelligentDialog(Dialog):
    def __init__(self, dialog_state: DialogState):
        self.dialog_state = dialog_state
        name_prompt = PromptDialog(
            self.dialog_state.get_subflow_dialog_state("name"),
            "Hi there. What's your name?",
        )
        choice_prompt = PromptDialog(
            self.dialog_state.get_subflow_dialog_state("choice"),
            "Do you want to talk about dragons or covid? answer 1 for dragons and 2 for covid.",
        )
        self.intro_dialog = DialogChain(
            self.dialog_state.get_subflow_dialog_state("intro"),
            [name_prompt, choice_prompt],
        )
        self.dragon_dialog = DialogChain(
            self.dialog_state.get_subflow_dialog_state("dragons"),
            [
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons1"),
                    "Do you like dragons?",
                ),
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons2"),
                    "Seriously, do you like dragons?",
                ),
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons3"),
                    "Good, because we REALLY Like dragons here. Wanna hear more?",
                ),
            ],
        )
        self.covid_dialog = DialogChain(
            self.dialog_state.get_subflow_dialog_state("dragons"),
            [
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons1"),
                    "How scary is covid?",
                ),
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons2"),
                    "Seriously, are you scared?",
                ),
                PromptDialog(
                    self.dialog_state.get_subflow_dialog_state("dragons3"),
                    "You're just playing though, right?",
                ),
            ],
        )

    def get_next_message(self, client_response):
        intro_response = self.intro_dialog.get_next_message(client_response)
        if not isinstance(intro_response, Done):
            return intro_response
        name, choice = intro_response.return_value

        if choice == "1":
            main_dialog = self.dragon_dialog
        else:
            main_dialog = self.covid_dialog

        main_dialog_response = main_dialog.get_next_message(client_response)
        if not isinstance(main_dialog_response, Done):
            return main_dialog_response

        return Done(return_value=f"Bye {name}! Hope you had fun!")


@dataclass
class ChatServer:
    main_dialog = IntelligentDialog(DialogState(InMemoryPersistence()))

    def get_server_message(self, client_response):
        server_response = self.main_dialog.get_next_message(client_response)
        return (
            server_response.response
            if isinstance(server_response, ServerResponse)
            else f"Ciao! {server_response.return_value}"
        )
