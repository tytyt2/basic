from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    categoryType = 'NW'

    class Meta:
        model = Post
        fields = ['author','title', 'text', 'rating']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     text = cleaned_data.get("text")
    #     title = cleaned_data.get("title")
    #
    #     if title == text:
    #         raise ValidationError(
    #             "Описание не должно быть идентично названию."
    #         )
    #
    #     return cleaned_data


class ArtForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    categoryType= 'AR'

    class Meta:
        model = Post
        fields = ['author','title', 'text', 'rating']