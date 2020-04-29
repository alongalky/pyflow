from dataclasses import dataclass
import random

from dialogs.types import RunSubdialog, Dialog
from dialogs.persistence import InMemoryPersistence
from dialogs.primitives import message, prompt, chain, multichoice, yes_no
from dialogs import run_dialog

DRAGON_DIALOG = chain(
    [
        prompt("Do you like dragons?"),
        prompt("Seriously, do you like dragons?"),
        message("Good, because we REALLY Like dragons here."),
        yes_no("Wanna hear more?", "Are you sure?"),
    ]
)
COVID_DIALOG = chain(
    [
        prompt("How scary is covid?"),
        prompt("Seriously, are you scared?"),
        message("I thought so."),
        prompt("You're just playing though, right?"),
    ]
)


class intelligent_dialog(Dialog):
    version = "1.0"

    def __call__(self, run: RunSubdialog):
        name = run(prompt("Hey! What's your name?"))
        random_animal = random.choice(
            ["turtle", "pokemon", "hummingbird", "caterpillar"]
        )
        run(
            chain(
                [
                    message("What a beautiful name!"),
                    message(f"I had a {random_animal} called {name} once."),
                    message(f"So, {name}, if that's your real name..."),
                ]
            )
        )

        interested = run(
            yes_no(
                "Would you like to talk to me today?",
                "A simple yes or no would be good.",
            )
        )
        if not interested:
            return

        choice = run(
            multichoice(
                f"What would you like to talk about?",
                f"Come on {name}! Now you know that's not valid. What will it be?",
                ["Dragons", "COVID"],
            )
        )

        if choice == 0:
            run(DRAGON_DIALOG)
        else:
            run(COVID_DIALOG)


@dataclass
class ChatServer:
    persistence = InMemoryPersistence()

    def get_server_messages(self, client_response):
        main_dialog = intelligent_dialog()

        for messages in run_dialog(main_dialog, self.persistence, client_response):
            return messages

        return ["Ciao!"]
