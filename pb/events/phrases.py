from datetime import date
import re

import attr

from . import responses


@attr.attrs
class _TextMatcher:
    text = attr.attrib()

    def matches(self, value):
        return self.text in value.lower()


@attr.attrs
class _RegexMatcher:
    _regex = attr.attrib()

    def matches(self, value):
        return re.match(self._regex, value.lower())


@attr.attrs
class _StaticResponse:
    _response = attr.attrib()

    @property
    def response(self):
        return self._response


@attr.attrs
class _DynamicResponse:
    _responses = attr.attrib()

    @property
    def response(self):        
        weekday = date.today().weekday()

        if weekday < len(self._responses):
            return self._responses[weekday]

        return responses.no_its_not


def _factory(*mixins):
    name = "".join(mixin.__name__ for mixin in mixins)
    return attr.make_class(name, ["identifier"], bases=mixins)


_StaticTextPhrase = _factory(_TextMatcher, _StaticResponse)
_StaticRegexPhrase = _factory(_RegexMatcher, _StaticResponse)
_DynamicRegexPhrase = _factory(_RegexMatcher, _DynamicResponse)

is_it_tuesday = _DynamicRegexPhrase(
    identifier='is_it_tuesday',
    regex=r'(är?)|e|ä d|(det?) tis+dag?\?+',
    responses=[
        responses.no_its_monday,
        responses.yes_its_hashtag_crazy,
        responses.no_its_wednesday,
    ],
)
pizza = _StaticTextPhrase(
    identifier='pizza',
    text='pizza',
    response=responses.did_you_say_pizza,
)
did_you_say_pizza = _StaticRegexPhrase(
    identifier='did_you_say_pizza',
    regex=r'hörde jag? pizza\?+',
    response=responses.oh_you_did,
)

_all = [
    is_it_tuesday,
    did_you_say_pizza,
    pizza,
]


def from_text(text):
    for phrase in _all:
        if phrase.matches(text):
            return phrase
