from dataclasses import dataclass

from dialogs.persistence import InMemoryPersistence, DialogState
from dialogs import prompt, chain


DRAGON_DIALOG = chain(
    [
        prompt("Do you like dragons?"),
        prompt("Seriously, do you like dragons?"),
        prompt("Good, because we REALLY Like dragons here. Wanna hear more?"),
    ]
)


COVID_DIALOG = chain(
    [
        prompt("How scary is covid?"),
        prompt("Seriously, are you scared?"),
        prompt("You're just playing though, right?"),
    ]
)


def intelligent_dialog(state, response):
    name = yield from prompt("Hey! What's your name?")(
        state.subflow_state("intro1"), response
    )
    _, choice = yield from chain(
        [
            prompt(f"Hello {name}!"),
            prompt(
                "Do you want to talk about dragons or covid? answer 1 for dragons and 2 for covid"
            ),
        ]
    )(state.subflow_state("intro2"), response)

    if choice == "1":
        is_like_dragons, is_seriously_like_dragons, is_wanna_hear_more = yield from DRAGON_DIALOG(
            state.subflow_state("dragons"), response
        )
    else:
        is_covid_scary, is_seriously_covid_scary, is_playing = yield from COVID_DIALOG(
            state.subflow_state("covid"), response
        )


@dataclass
class ChatServer:
    state = DialogState(InMemoryPersistence())

    def get_server_message(self, client_response):
        main_dialog = intelligent_dialog

        for server_response in main_dialog(self.state, client_response):
            return server_response

        return "Ciao!"
