from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from pb.slack.api.calls import channel_info


def message_in_channel(channel_id, match_channel):
    response = channel_info(channel_id)
    
    if response.get('ok'):
        channel_name = response['channel']['name']
        return channel_name == match_channel

    return False


def require_verification_token(view_method):
    def decorated_view(view, request, *args, **kwargs):
        if not request.data.get('verification_token') == settings.SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return view_method(view, request, *args, **kwargs)

    return decorated_view


def url_verification(view_method):
    def decorated_view(view, request, *args, **kwargs):
        if request.data.get('type') == 'url_verification':
            challenge = request.data.get('challenge')
            return Response(data={'challenge': challenge})

    return decorated_view
