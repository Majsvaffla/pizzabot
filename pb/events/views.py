from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slackclient import SlackClient

from django.conf import settings


slack_client = SlackClient(settings.SLACK_BOT_USER_TOKEN)


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if not slack_message.get('token') == settings.SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        if 'event' in slack_message:
            event_message = slack_message.get('event')

            if event_message.get('subtype') == 'bot_message':
                return Response(status=status.HTTP_200_OK)

            text = event_message.get('text')
            channel = event_message.get('channel')
            bot_text = 'Ja, det är #crazy-tuesday! :pizza:'

            if 'är det tisdag' in text.lower():
                slack_client.api_call(
                    method='chat.postMessage',
                    channel=channel,
                    text=bot_text,
                )

                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
