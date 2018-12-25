import datetime

import pytest
from freezegun import freeze_time

from pb.events import phrases, responses


@pytest.mark.parametrize("date, expected_response", [
    (datetime.date(2018, 7, 23), 'Nej, det är bara måndag :soon:'),
    (datetime.date(2018, 7, 24), 'Ja, det är #crazy-tuesday! :pizza:'),
    (datetime.date(2018, 7, 25), 'Nej, det är onsdag :cry:'),
    (datetime.date(2018, 7, 26), 'Nej, det är det inte :sad:'),
])
def test_is_it_tuesday(date, expected_response):
    with freeze_time(date):
        response = phrases.is_it_tuesday.response
        assert response.text == expected_response


def test_pizza():
    response = phrases.pizza.response
    assert response.text == "Hörde jag :pizza:?"


class Test_from_text:
    def test_text_phrase(self):
        assert phrases.from_text("pizza") is phrases.pizza

    def test_regex_phrase(self):
        assert phrases.from_text("hörde ja pizza?????") is phrases.did_you_say_pizza
