from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import formset_factory, modelformset_factory, Textarea, TextInput, CheckboxInput
from tinymce.widgets import TinyMCE


class AddQuestionForm(ModelForm):
    class Meta:
        model = Version
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        fields = ["razdatka",
                  "text",
                  "answer",
                  "also_answer",
                  "not_answer",
                  "commentary",
                  "sources"]

class EditQuestionForm(ModelForm):
    class Meta:
        model = Version
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        fields = ["id",
                  "razdatka",
                  "text",
                  "answer",
                  "also_answer",
                  "not_answer",
                  "commentary",
                  "sources",
                  "editor_comments"]

class EditTestForm(ModelForm):
    class Meta:
        model = Test
        exclude = ["user"]
        widgets = {'tournament': forms.CheckboxSelectMultiple()}

class EditTesterForm(ModelForm):
    class Meta:
        model = Tester
        exclude = ["test", "user"]

class EditTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        exclude = ["user"]

class EditVersionComment(ModelForm):
    pk = forms.IntegerField()
    class Meta:
        model = Version
        fields = ["editor_comments"]
        widgets = {'editor_comments': TinyMCE()}

class RateQuestion(ModelForm):
    class Meta:
        model = TestQuestion
        fields = ["rating", "test", "question"]
        widgets = {'test': forms.HiddenInput(),
                   'question': forms.HiddenInput()}

class IsAnsweredQuestion(ModelForm):
    class Meta:
        model = TestQuestion
        fields = ["is_answered", "test", "question"]
        widgets = {'test': forms.HiddenInput(),
                   'question': forms.HiddenInput()}

VersionFormSet = modelformset_factory(
    Version,
    exclude = ["question", "created"],
    widgets={
        "text": TinyMCE(attrs={'cols': 80, 'rows': 30}),
        "editor_comments": TinyMCE(attrs={'cols': 50, 'rows': 10})
    },
    extra=0
)

