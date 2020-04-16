from dataclasses import dataclass

from dialogs.persistence import InMemoryPersistence, DialogState
from dialogs.primitives import prompt, chain, multichoice
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
    name = yield from run("intro1", prompt("Hey! What's your name?"))
    choice = yield from run(
        "intro2",
        multichoice(
            f"Hey {name}! What would you like to talk about?",
            f"Come on {name}! Now you know that's not valid. What will it be?",
            ["Dragons", "COVID"],
        ),
    )

    if choice == 0:
        likes, really_likes, hear_more = yield from run("dragons", DRAGON_DIALOG)
    else:
        scary, really_scaring, is_playing = yield from run("covid", COVID_DIALOG)


@dataclass
class ChatServer:
    state = DialogState(InMemoryPersistence())

    def get_server_message(self, client_response):
        main_dialog = intelligent_dialog

        for server_response in run_dialog(main_dialog, self.state, client_response):
            return server_response

        return "Ciao!"
