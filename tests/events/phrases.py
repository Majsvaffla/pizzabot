import datetime

import pytest
from freezegun import freeze_time

from pb.events import phrases, responses


@pytest.mark.parametrize("date, expected_response", [
    (datetime.date(2018, 7, 23), 'Nej, det är bara måndag :soon:'),
    (datetime.date(2018, 7, 24), f'Ja, det är #crazy-tuesday! :pizza:'),
    (datetime.date(2018, 7, 25), 'Nej, det är onsdag :cry:'),
    (datetime.date(2018, 7, 25), 'Nej, det är det inte :sad:'),
])
def test_is_it_tuesday(date, expected_response):
    with freeze_time(date):
        response responses.from_phrase(phrases.is_it_tuesday)
        assert response.text == expected_response


def test_pizza():
    response = responses.from_phrase(phrase.pizza)
    assert response.text == "Hörde jag :pizza:?"
