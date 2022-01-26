import re

from django.forms.models import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name','project',)


