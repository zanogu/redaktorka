from django import template
import json
from bs4 import BeautifulSoup
from pprint import pprint
from my_questions.models import *


from django.template.context_processors import request

from my_questions.models import Question

register = template.Library()
from django.forms.models import model_to_dict

@register.filter
def whats_inside(value):
    print("INSIDE")
    pprint(vars(value))
    return value

@register.filter
def tester_list(value):
    return ", ".join([t.name_surname for t in value])


@register.filter
def model_to_dict_filter(value):
    return json.dumps(model_to_dict(value), default=str)

@register.filter
def elochki(value):
    opened = False
    value = list(value)
    for i in range(len(value)):
        if (value[i] == "\"" or value[i] == "„") and not opened:
            value[i] = "«"
            opened = True
        elif value[i] == "\"" or value[i] == "“":
            value[i] = "»"
            opened = False
    return "".join(value)

@register.filter
def extract_text_from_html(value):
    soup = BeautifulSoup(value, 'html.parser')
    for data in soup(['style', 'script']):
        data.decompose()
    return " ".join(soup.stripped_strings)


def latest_version(value):
    if not isinstance(value, Question):
        raise TypeError("latest_version requires Question instance")
    try:
        return value.version_set.latest('created')
    except Version.DoesNotExist:
        return Version(text="нет версий", question=value)

@register.filter
def latest_version_text(value):
    return extract_text_from_html(latest_version(value).text)

@register.filter
def latest_version_answer(value):
    return latest_version(value).answer

@register.filter
def latest_version_razdatka(value):
    return latest_version(value).razdatka