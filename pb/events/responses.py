from datetime import date

import attr

from . import phrases


@attr.attrs
class _Response:
    identifier = attr.attrib()
    text = attr.attrib()


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
    text='Ja, det är #crazy_tuesday! :pizza:',
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
    text='Hörde jag :pizza:?'
)


def from_phrase(phrase):
    if phrase == phrases.is_it_tuesday:
        weekday = date.today().isoweekday()

        if weekday == 1:
            return no_its_monday
        elif weekday == 2:
            return yes_its_hashtag_crazy
        elif weekday == 3:
            return no_its_wednesday
        else:
            return no_its_not

    if phrase == phrases.pizza:
        return did_you_say_pizza
