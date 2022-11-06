# from dataclasses import field
# from pyexpat import model
from django.forms import ModelForm
from .models import MyImage
from django import forms


class ImageForm(forms.ModelForm):

    class Meta:
        model=MyImage
        fields=['caption','image']