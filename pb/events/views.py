from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pb.slack.api.calls import post_message

from . import phrases
from . import responses
from .constants import PIZZA_CHANNEL
from .utils import (
    message_in_channel,
    require_verification_token,
    url_verification,
)


class Events(APIView):
    @require_verification_token
    @url_verification
    def post(self, request, *args, **kwargs):
        if 'event' in request.data:
            event = request.data.get('event')

            if event.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            channel = event.get('channel')

            if event.get('type') == 'message' and message_in_channel(channel, PIZZA_CHANNEL):
                text = event.get('text')
                phrase = phrases.from_text(text)

                # if phrase is not None:
                response = phrase.response

                if response is not None and response.cool:
                    post_message(text=response.text)

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
