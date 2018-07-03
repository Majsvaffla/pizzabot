from slackclient import SlackClient

from django.conf import settings


slack_client = SlackClient(settings.SLACK_BOT_USER_TOKEN)


def message_in_channel(channel_id, match_channel):
    response = slack_client.api_call(
        method='channels.info',
        channel=channel_id,
    )
    
    if response.get('ok'):
        channel_name = response['channel']['name']
        return channel_name == match_channel

    return False
