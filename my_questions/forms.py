from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import formset_factory, modelformset_factory

class AddQuestionForm(ModelForm):
    class Meta:
        model = Version
        fields = ["razdatka", "text", "answer", "also_answer", "not_answer","commentary", "sources"]

class EditQuestionForm(ModelForm):
    class Meta:
        model = Version
        fields = ["id", "razdatka", "text", "answer", "also_answer", "not_answer","commentary", "sources"]

class EditTesterForm(ModelForm):
    class Meta:
        model = Tester
        exclude = ["test", "user"]

VersionFormSet = modelformset_factory(Version, exclude = ["question", "created"] )