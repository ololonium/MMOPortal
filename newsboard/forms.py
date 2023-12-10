from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'role', 'content']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')

        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Текст отклика:"
