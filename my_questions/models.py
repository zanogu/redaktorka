from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField
from tinymce.models import HTMLField



# Create your models here.

class Question(models.Model):
    created = models.DateTimeField()
    last_edited = models.DateTimeField()
    user = models.ManyToManyField(User)


class Version(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    razdatka = models.ImageField(upload_to = "my_questions/static/my_questions/uploads/",blank=True)
    text = models.TextField()
    answer = EncryptedCharField(blank=True)
    also_answer = EncryptedCharField(blank=True)
    not_answer = EncryptedCharField(blank=True)
    commentary = EncryptedTextField(blank=True)
    sources = EncryptedTextField(blank=True)
    created = models.DateTimeField()
    last_edited = models.DateTimeField(blank=True)

    class Meta:
        ordering = ["-created"]


class Test(models.Model):
    date = models.DateField(blank=True)
    name = models.CharField(blank=True)
    description = models.TextField(blank=True)
    version = models.ManyToManyField(Version)
    question = models.ManyToManyField(Question, through="TestQuestion")
    user = models.ManyToManyField(User)

    def __str__(self):
        return str(model_to_dict(self))

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()

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
