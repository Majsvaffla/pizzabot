from datetime import datetime

from freezegun import freeze_time

from pb.events import responses


def test_cool_pizza():
    responses.did_you_say_pizza.cool = True

    with freeze_time(datetime(2018, 8, 15, 10, 30)):
        response = responses.did_you_say_pizza
        assert response.cool
        response.text
        assert not response.cool

    with freeze_time(datetime(2018, 8, 15, 10, 35, 1)):
        assert response.cool
