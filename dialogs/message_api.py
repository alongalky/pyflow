import threading
import uuid

from dataclasses import dataclass

outgoing_messages = []
incoming_messages = {}

@dataclass
class MessageRequest:
    text: str
    token: str = uuid.uuid4()


@dataclass
class MessageResponse:
    ref_token: str
    text: str

class MessagingAPI:

    @staticmethod
    def get_outgoing_message_queue():
        return outgoing_messages

    @staticmethod
    def get_incoming_message_queue():
        return incoming_messages

    @staticmethod
    def send_message(text:str) -> MessageRequest:
        outgoing_messages = MessagingAPI.get_outgoing_message_queue()
        msg =  MessageRequest(text)
        outgoing_messages.append(msg)
        return msg

    @staticmethod
    def receive_message(text:str, token:str) -> MessageResponse:
        incoming_messages = MessagingAPI.get_incoming_message_queue()
        msg = MessageResponse(ref_token=token, text=text)
        incoming_messages[msg.ref_token] = msg
        return msg

    @staticmethod
    def consume_response_for(token:str) -> MessageResponse:
        incoming_messages = MessagingAPI.get_incoming_message_queue()
        res = incoming_messages.get(token, None)
        if res:
            incoming_messages.pop(token)
        return res

    @staticmethod
    def consume_outbound_message()-> MessageRequest:
        result = []
        result.extend(outgoing_messages)
        outgoing_messages.clear()
        return result

