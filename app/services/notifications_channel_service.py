import uuid
import logging
from protorpc import messages
from ferris3 import Service, hvild, auto_service, auto_method
from app.models.data import Data
from app.models.database import session
from google.appengine.api import channel


class ResponseMessage(messages.Message):
    token = messages.StringField(1)
    email = messages.StringField(2)


class RequestMessage(messages.Message):
    email = messages.StringField(1)
    application = messages.StringField(2)


class SendMessage(messages.Message):
    channel = messages.StringField(1)
    application = messages.StringField(2)
    message = messages.StringField(3)


@auto_service(endpoint="ferris", path="collections")
class NotificationsChannelService(Service):
    @auto_method(http_method="POST", name="create_channel", returns=ResponseMessage)
    def create_channel(self, request=(RequestMessage,)):
        email = getattr(request, 'email')
        token = channel.create_channel(email)
        logging.warning(token)

        return ResponseMessage(
            token=token,
            email=email)

    @auto_method(http_method="POST", name="send_notification", returns=ResponseMessage)
    def send_notification(self, request=(SendMessage,)):
        channel.send_message(
            getattr(request, 'email'),
            getattr(request, 'message'))

