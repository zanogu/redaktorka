from django.http import HttpRequest

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from django.urls import reverse


def simple_permissions_check(request: HttpRequest) -> bool:
    return True

class MainNav(Nav):
    template_name = "my_questions/parts/header.html"
    items = [
        NavItem(title="Вопросы", url="my_questions:questions_list_view"),
        NavItem(title="Добавить вопрос", url="my_questions:add_question", extra_context={"class": "menu-split"}),
        NavItem(title="Тестеры", url="my_questions:testers_view", extra_context={"class": "menu-split"}),
        NavItem(title="Тесты", url=f"my_questions:test_list_view"),
        NavItem(title="Cоздать Тест", url="my_questions:create_test_view", extra_context={"class": "menu-split"}),
    ]

