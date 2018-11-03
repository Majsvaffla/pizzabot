from datetime import datetime
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from pb_test.fixtures import dummy_view_class

from pb.events import phrases, responses
from pb.events.utils import (
    in_channel,
    message_in_channel,
    post_response_from_phrase,
    require_verification_token,
    url_verification,
)
from pb.slack.api.calls import APICall


@pytest.fixture
def event_factory():
    return {
        'event': {
            'channel': 'S0M3_CH4NN3L_1D',
            'type': 'message',
            'text': 'H3ll0'
        }
    }

@pytest.fixture
def request_factory():
    def decorator(request_data):
        class Request:
            data = request_data

        return Request()

    return decorator


def mock_channel_info(channel_name):
    def channel_info(*args, **kwargs):
        return {
            'ok': True,
            'channel': {
                'name': channel_name
            }
        }

    return channel_info


class Test_in_channel:
    @patch('pb.events.utils.channel_info', mock_channel_info('Coco'))
    def test_in_channel(self):
        assert in_channel('S0M3_CH4NN3L_1D', 'Coco')

    @patch('pb.events.utils.channel_info', mock_channel_info('This is not the channel you are looking for.'))
    def test_not_in_channel(self):
        assert not in_channel('S0M3_CH4NN3L_1D', 'Coco')


class Test_message_in_channel:

    @pytest.mark.parametrize('request_data, expected_status', [
        (
            {
                'event': {
                    'subtype': 'bot_message'
                }
            },
            status.HTTP_200_OK,
        ),
        (
            {},
            status.HTTP_400_BAD_REQUEST,
        ),
    ])
    def test_no_message(self, dummy_view_class, request_factory, request_data, expected_status):
        DummyViewClass = dummy_view_class(Response(status=status.HTTP_302_FOUND))    
        view = DummyViewClass()
        wrapper = message_in_channel('Some channel')
        decorated_view = wrapper(DummyViewClass.view_method)
        request = request_factory(request_data)
        response = decorated_view(view, request)

        assert response.status_code == expected_status


    @patch('pb.events.utils.channel_info', mock_channel_info('Coco'))
    def test_message_in_channel(self, dummy_view_class, request_factory, event_factory):
        DummyViewClass = dummy_view_class(Response(status=status.HTTP_302_FOUND))    
        view = DummyViewClass()
        wrapper = message_in_channel('Coco')
        decorated_view = wrapper(DummyViewClass.view_method)
        request = request_factory(event_factory)
        response = decorated_view(view, request)

        assert response.status_code == status.HTTP_302_FOUND

    @patch('pb.events.utils.channel_info', mock_channel_info('This is not the channel you are looking for.'))
    def test_not_in_channel(self, dummy_view_class, request_factory, event_factory):
        DummyViewClass = dummy_view_class(Response(status=status.HTTP_302_FOUND))    
        view = DummyViewClass()
        wrapper = message_in_channel('Coco')
        decorated_view = wrapper(DummyViewClass.view_method)
        request = request_factory(event_factory)
        response = decorated_view(view, request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize('verification_token, expected_status', [
    (settings.SLACK_VERIFICATION_TOKEN, status.HTTP_200_OK),
    ('invalid_verification_token', status.HTTP_403_FORBIDDEN),
])
def test_require_virification_token(dummy_view_class, request_factory, verification_token, expected_status):
    DummyViewClass = dummy_view_class(Response(status=status.HTTP_200_OK))    
    view = DummyViewClass()
    decorated_view = require_verification_token(DummyViewClass.view_method)
    request = request_factory({
        'token': verification_token,
    })
    response = decorated_view(view, request)

    assert response.status_code == expected_status


@pytest.mark.parametrize('event_type, challenge, expected_data', [
    ('url_verification', '1+x=2', {'challenge': '1+x=2'}),
    ('not_url_verification', None, {}),
])
def test_url_verification(dummy_view_class, request_factory, event_type, challenge, expected_data):
    DummyViewClass = dummy_view_class(Response(data={}))
    view = DummyViewClass()
    decorated_view = url_verification(DummyViewClass.view_method)
    request = request_factory({
        'type': event_type,
        'challenge': challenge,
    })
    response = decorated_view(view, request)

    assert response.data == expected_data


@patch('pb.events.utils.post_message', APICall('api.test'))
class Test_post_response_from_phrase:
    def test_single_message(self):
        phrases.pizza.response.cool = True
        response = post_response_from_phrase(phrases.pizza)
        assert response['ok']

    def test_recurring_message(self):
        phrases.pizza.response.cool = True

        with freeze_time(datetime(2018, 8, 15, 10, 29)):
            response = post_response_from_phrase(phrases.pizza)
            assert response['ok']

        with freeze_time(datetime(2018, 8, 15, 10, 30)):
            response = post_response_from_phrase(phrases.pizza)
            assert response is None

        with freeze_time(datetime(2018, 8, 15, 10, 36)):
            response = post_response_from_phrase(phrases.pizza)
            assert response['ok']
