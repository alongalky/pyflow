import sys

from dialogs.message_api import MessagingAPI
from example.chat_server import ChatServer


def get_client_response():
    return sys.stdin.readline()


def main():
    chat_server = ChatServer()
    client_response = None
    server_message = None
    while not server_message or not server_message.text.lower().startswith("ciao"):
        chat_server.get_server_message()
        server_messages = MessagingAPI.consume_outbound_message()
        token = ""
        for m in server_messages:
            print("Server:", m.text)
            #lst message token
            token = m.token
            server_message = m
        if server_message and not server_message.text.lower().startswith("ciao"):
            client_response_text = get_client_response().strip()
            if token:
                client_response = MessagingAPI.receive_message(client_response_text, token)

if __name__ == "__main__":
    main()
