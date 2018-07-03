from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slackclient import SlackClient

from django.conf import settings

from . import phrases
from . import responses


slack_client = SlackClient(settings.SLACK_BOT_USER_TOKEN)


class Events(APIView):
    def post(self, request, *args, **kwargs):
        if not request.data.get('token') == settings.SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if request.data.get('type') == 'url_verification':
            challenge = request.data.get('challenge')
            return Response(data={'challenge': challenge})

        if 'event' in request.data:
            event = request.data.get('event')

            if event.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            text = event.get('text')
            channel = event.get('channel')
            
            def api_call(response):
                slack_client.api_call(
                    method='chat.postMessage',
                    channel=channel,
                    text=response.text,
                )

            phrase = phrases.from_text(text)
            response = responses.from_phrase(phrase)

            if response is not None:
                api_call(response)

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
