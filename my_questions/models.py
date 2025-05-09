from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
from typing import List
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Question(models.Model):
    created = models.DateTimeField()
    last_edited = models.DateTimeField()
    user = models.ManyToManyField(User)
    author = models.CharField(default='')

    @property
    def related_committed_tests(self) -> List:
        return self.tests.filter(committed=True)

    @property
    def testers(self) -> List:
        return Tester.objects.filter(test__in=self.related_committed_tests)


class Version(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    razdatka = models.FileField(upload_to = "my_questions/static/my_questions/uploads/",blank=True)
    text = models.TextField()
    answer = EncryptedCharField(blank=True)
    also_answer = EncryptedCharField(blank=True)
    not_answer = EncryptedCharField(blank=True)
    commentary = EncryptedTextField(blank=True)
    sources = EncryptedTextField(blank=True)
    created = models.DateTimeField()
    last_edited = models.DateTimeField(blank=True, null = True)
    editor_comments = models.TextField(blank=True, null=True)

    @property
    def related_committed_tests(self) -> List:
        return self.tests.filter(committed = True)

    @property
    def is_part_of_committed_tests(self) -> bool:
        return len(self.related_committed_tests) > 0

    class Meta:
        ordering = ["-created"]


class Tournament(models.Model):
    tournament_rating_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=400)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    id_season = models.IntegerField(null=True, blank=True)
    type_id = models.IntegerField(null=True, blank=True)
    type_name = models.CharField(null=True, blank=True)
    question_quantity = models.JSONField(default={"1":12, "2": 12, "3": 12})
    truedl = models.FloatField(default = 0)
    user = models.ManyToManyField(User)

    @property
    def question_quantity_general(self) -> int:
        return sum([v for v in self.question_quantity.values()])

    @property
    def tours_quantity(self) -> int:
        return len(self.question_quantity.keys())

    @property
    def tour_length(self) -> int:
        return list(self.question_quantity.values())[0]

    def __str__(self):
        return f"{self.tournament_rating_id}: {self.name}"


class Test(models.Model):
    date = models.DateField(blank=True)
    name = models.CharField(blank=True)
    description = models.TextField(blank=True)
    version = models.ManyToManyField(Version, blank=True, null = True, related_name="tests")
    question = models.ManyToManyField(Question, through="TestQuestion", related_name="tests")
    user = models.ManyToManyField(User)
    editor_comments = models.TextField(blank=True, null = True)
    committed = models.BooleanField(default=False)
    committed_datetime = models.DateTimeField(blank=True, null = True)
    tournament = models.ManyToManyField(Tournament, blank=True, null = True, related_name="tests")

    def __str__(self):
        return str(model_to_dict(self))

class TestQuestion(models.Model):
    RATING_CHOICES = [(-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3)]
    class IsAnswered(models.TextChoices):
        ANSWERED_MINUTE = "AM", _("Ответили в минуте")
        ANSWERED = "AN", _("Ответили")
        ANSWERED_HELP = "AH", _("Оветили с подсказкой")
        NOT_ANSWERED = "NA", _("Не ответили")
        NO_KNOWLEDGE = "NK", _("Нет свояка")

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    is_answered = models.CharField(
        max_length=2,
        choices=IsAnswered,
        blank=True,
        null=True
    )
    rating = models.IntegerField(
        blank=True, null=True, choices = RATING_CHOICES)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["test", "question"], name="unique_test_question"
            )
        ]


class Tester(models.Model):
    name = models.CharField()
    surname = models.CharField()
    patronymic = models.CharField(blank=True, null=True)
    rating_id = models.IntegerField(blank=True, null=True)
    test = models.ManyToManyField(Test, blank=True, related_name="testers")
    user = models.ManyToManyField(User)

    @property
    def name_surname(self) -> str:
        return " ".join([str(self.name), str(self.surname)])

    @property
    def surname_name(self) -> str:
        return " ".join([str(self.surname), str(self.name)])

    class Meta:
        ordering = ["surname", "name"]

    def __str__(self):
        return self.surname_name
