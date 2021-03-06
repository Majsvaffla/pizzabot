import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import phrases
from .constants import PIZZA_CHANNEL
from .utils import (
    message_in_channel,
    post_response_from_phrase,
    require_verification_token,
    url_verification,
)


logger = logging.getLogger(__name__)

class Events(APIView):
    @require_verification_token
    @url_verification
    @message_in_channel(PIZZA_CHANNEL)
    def post(self, request, message):
        phrase = phrases.from_text(message)

        if phrase is not None:
            post_response_from_phrase(phrase)

        return Response(status=status.HTTP_200_OK)
