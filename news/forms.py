from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'

        fields = [
            'type',
            'title',
            'body',
            'author',
            'cats',
        ]

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        if body is not None and len(body) < 20:
            raise ValidationError({
                "body": "Текст поста не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == body:
            raise ValidationError(
                "Название не должно совпадать с основным текстом."
            )
        return cleaned_data
