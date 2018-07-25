from slackclient import SlackClient

from django.conf import settings

from pb.events.constants import PIZZA_CHANNEL


class APICall:
    _client = SlackClient(settings.SLACK_BOT_USER_TOKEN)

    def __init__(self, method, **call_kwargs):
        self._method = method
        self._call_kwargs = call_kwargs

    def __call__(self, **data):
        return self._client.api_call(
            **self._params,
            **data,
        )

    def __str__(self):
        return self._method

    @property
    def _params(self):
        return {
            'method': self._method,
            **self._call_kwargs,
        }

    @property
    def json(self):
        return self._client.server.api_call(**self._params)


post_message = APICall(
    method='chat.postMessage',
    channel=PIZZA_CHANNEL,
)
channel_info = APICall(
    method='channels.info',
)
