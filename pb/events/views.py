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
    @message_in_channel(PIZZA_CHANNEL)
    def post(self, request, message):
        phrase = phrases.from_text(message)

        if phrase is not None:
            response = phrase.response

            if response is not None and response.cool:
                post_message(text=response.text)

        return Response(status=status.HTTP_200_OK)
