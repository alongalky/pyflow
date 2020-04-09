import sys
from chat_server import ChatServer


def get_client_response():
    return sys.stdin.readline()


def main():
    chat_server = ChatServer()
    client_response = ""
    server_message = ""
    while not server_message.lower().startswith("ciao"):
        server_message = chat_server.get_server_message(client_response)
        print("Server:", server_message)
        client_response = get_client_response().strip()


if __name__ == "__main__":
    main()
