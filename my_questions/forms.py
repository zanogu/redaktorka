from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import formset_factory, modelformset_factory, Textarea, TextInput, CheckboxInput
from tinymce.widgets import TinyMCE


class AddQuestionForm(ModelForm):
    class Meta:
        model = Version
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        fields = ["razdatka", "text", "answer", "also_answer", "not_answer","commentary", "sources"]

class EditQuestionForm(ModelForm):
    class Meta:
        model = Version
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}
        fields = ["id", "razdatka", "text", "answer", "also_answer", "not_answer","commentary", "sources"]

class EditTesterForm(ModelForm):
    class Meta:
        model = Tester
        exclude = ["test", "user"]

VersionFormSet = modelformset_factory(Version, exclude = ["question", "created"], widgets={"text": TinyMCE(attrs={'cols': 80, 'rows': 30})} )