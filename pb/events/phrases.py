import attr

from . import responses


@attr.attrs
class _Phrase:
    identifier = attr.attrib()
    text = attr.attrib()


is_it_tuesday = _Phrase(
    identifier='is_it_tuesday',
    text='är det tisdag',
)
pizza = _Phrase(
    identifier='pizza',
    text='pizza',
)

_all = [
    is_it_tuesday,
    pizza,
]
_text_map = {p.text: p for p in _all}


def from_text(text):
    for phrase in _all:
        if phrase.text in text.lower():
            return phrase
