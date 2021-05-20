from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Project


class CreateProjectForm(forms.Form):
    project_name = forms.CharField(label='_(Project name)', max_length=100)
