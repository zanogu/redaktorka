from django import template
import json
from bs4 import BeautifulSoup

from django.template.context_processors import request

register = template.Library()
from django.forms.models import model_to_dict


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



