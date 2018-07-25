import attr

from . import responses


@attr.attrs
class _Phrase:
    identifier = attr.attrib()
    text = attr.attrib()


@attr.attrs
class _StaticResponsePhrase(_Phrase):
    _response = attr.attrib()

    @property
    def response(self):
        return self._response


@attr.attrs
class _DynamicResponsePhrase(_Phrase):
    _responses = attr.attrib()

    @property
    def response(self):        
        weekday = date.today().weekday()

        if weekday < len(self._responses):
            return self._responses[weekday]

        return no_its_not


is_it_tuesday = _DynamicResponsePhrase(
    identifier='is_it_tuesday',
    text='är det tisdag',
    responses=[
        responses.no_its_monday,
        responses.yes_its_hashtag_crazy,
        responses.no_its_wednesday,
    ],
)
pizza = _StaticResponsePhrase(
    identifier='pizza',
    text='pizza',
    response=responses.did_you_say_pizza,
)

_all = [
    is_it_tuesday,
    pizza,
]


def from_text(text):
    for phrase in _all:
        if phrase.text in text.lower():
            return phrase
