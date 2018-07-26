from datetime import date, datetime

import attr

from . import phrases
from .constants import PIZZA_CHANNEL, RESPONSE_DEFAULT_TIMEOUT


@attr.attrs
class _Response:
    identifier = attr.attrib()
    _text = attr.attrib()
    _timeout = attr.attrib(default=RESPONSE_DEFAULT_TIMEOUT)
    _last_used_at = datetime.min

    @property
    def text(self):
        self._last_used_now()
        return self._text

    @property
    def cool(self):
        return self._last_used_at + self._timeout < datetime.now()

    def _last_used_now(self):
        self._last_used_at = datetime.now()


yes_it_is = _Response(
    identifier='yes_it_is',
    text='Ja, det är det!',
)
yes_its_crazy = _Response(
    identifier='yes_its_crazy',
    text='Ja, det är Crazy Tuesday! :pizza:',
)
yes_its_hashtag_crazy = _Response(
    identifier='yes_its_hashtag_crazy',
    text=f'Ja, det är #{PIZZA_CHANNEL}! :pizza:',
)
no_its_not = _Response(
    identifier='no_its_not',
    text='Nej, det är det inte :sad:',
)
no_its_monday = _Response(
    identifier='no_its_not',
    text='Nej, det är bara måndag :soon:',
)
no_its_wednesday = _Response(
    identifier='no_its_wednesday',
    text='Nej, det är onsdag :cry:',
)
no_its_wacky_wednesday = _Response(
    identifier='no_its_wacky_wednesday',
    text='Nej, men det är Wacky Wednesday! :pizza:'
)
did_you_say_pizza = _Response(
    identifier='did_you_say_pizza',
    text='Hörde jag :pizza:?',
    timeout=300,
)
