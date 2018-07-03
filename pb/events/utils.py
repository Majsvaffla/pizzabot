def message_in_channel(channel_id, match_channel):
    channel = slack_client.api_call(
        method='channels.info',
        channel=channel_id,
    )
    channel_name = channel.get('name')
    return channel_name == match_channel
