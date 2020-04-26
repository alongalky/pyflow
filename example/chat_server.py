from dataclasses import dataclass

from dialogs.message_api import MessagingAPI
from dialogs.persistence import InMemoryPersistence, DialogState
from dialogs.primitives import prompt, chain #, multichoice, yes_no
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


def intelligent_dialog(run, state):

    name = yield from run(prompt("Hey! What's your name?"))
    topic = yield from run(prompt(f"Hey {name}. Would you like to talk to me today?"))

    if topic and len(topic)>10:
         MessagingAPI.send_message("this is too long for me...")
    else:
        MessagingAPI.send_message("this is too short for me...")

    return None

@dataclass
class ChatServer:
    state = DialogState(InMemoryPersistence())

    def get_server_message(self):
        main_dialog = intelligent_dialog
        for server_response in run_dialog(main_dialog, self.state):
            return server_response
        MessagingAPI.send_message("Ciao!!")




