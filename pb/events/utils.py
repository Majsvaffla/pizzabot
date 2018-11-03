import logging

from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from pb.slack.api.calls import channel_info, post_message


logger = logging.getLogger(__name__)

def in_channel(channel_id, match_channel):
    response = channel_info(channel=channel_id)

    if response.get('ok'):
        channel_name = response['channel']['name']
        return channel_name == match_channel

    return False


def message_in_channel(channel_name):    
    def wrapper(view_method):
        def decorated_view(view, request, *args, **kwargs):
            if 'event' in request.data:
                event = request.data.get('event')
                unwanted_subtypes = ['bot_message', 'message_deleted']

                if event.get('subtype') in unwanted_subtypes:
                    return Response(status=status.HTTP_200_OK)

                channel = event.get('channel')

                if event.get('type') == 'message' and in_channel(channel, channel_name):
                    text = event.get('text')

                    logger.info(f'Channel "{channel_name}" received message: {text}')

                    return view_method(view, request, text, *args, **kwargs)

            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return decorated_view

    return wrapper


def require_verification_token(view_method):
    def decorated_view(view, request, *args, **kwargs):
        token = request.data.get('token')

        if not token == settings.SLACK_VERIFICATION_TOKEN:
            logger.info(f'Verification token did not match ({token})')
            return Response(status=status.HTTP_403_FORBIDDEN)

        return view_method(view, request, *args, **kwargs)

    return decorated_view


def url_verification(view_method):
    def decorated_view(view, request, *args, **kwargs):
        if request.data.get('type') == 'url_verification':
            logger.info('Got URL verification event')
            challenge = request.data.get('challenge')
            return Response(data={'challenge': challenge})

        return view_method(view, request, *args, **kwargs)

    return decorated_view


def post_response_from_phrase(phrase):
    response = phrase.response

    if response is not None:
        if response.cool:
            logger.info('Responding with: {response.text}')
            return post_message(text=response.text)
        else:
            logger.info(f'Response not cool yet')
