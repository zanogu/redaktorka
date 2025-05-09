from django.http import HttpRequest

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from django.urls import reverse
from my_questions.constants import *


def simple_permissions_check(request: HttpRequest) -> bool:
    return True

class MainNav(Nav):
    template_name = "my_questions/parts/header.html"
    items = [
        NavItem(title=TERMS["questions"], url="my_questions:questions_list_view"),
        NavItem(title=TERMS["add_question"], url="my_questions:add_question", extra_context={"class": "menu-split"}),
        NavItem(title=TERMS["testers"], url="my_questions:testers_view"),
        NavItem(title=TERMS["tournaments"], url="my_questions:tournaments_view", extra_context={"class": "menu-split"}),
        NavItem(title=TERMS["tests"], url=f"my_questions:test_list_view"),
        NavItem(title=TERMS["add_test"], url="my_questions:create_test_view", extra_context={"class": "menu-split"}),
    ]

