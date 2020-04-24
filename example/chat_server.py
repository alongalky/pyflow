from dataclasses import dataclass

from dialogs.persistence import InMemoryPersistence
from dialogs.primitives import prompt, chain, multichoice, yes_no
from dialogs import run_dialog

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


def intelligent_dialog(run, state, response):
    name = yield from run(prompt("Hey! What's your name?"))

    interested = yield from run(
        yes_no(
            f"Hey {name}. Would you like to talk to me today?",
            f"A simple yes or no would be good.",
        )
    )
    if not interested:
        return

    choice = yield from run(
        multichoice(
            f"What would you like to talk about?",
            f"Come on {name}! Now you know that's not valid. What will it be?",
            ["Dragons", "COVID"],
        )
    )

    if choice == 0:
        likes, really_likes, hear_more = yield from run(DRAGON_DIALOG)
    else:
        scary, is_scared, is_playing = yield from run(COVID_DIALOG)


@dataclass
class ChatServer:
    persistence = InMemoryPersistence()

    def get_server_message(self, client_response):
        main_dialog = intelligent_dialog

        for server_response in run_dialog(
            main_dialog, self.persistence, client_response
        ):
            return server_response

        return "Ciao!"
