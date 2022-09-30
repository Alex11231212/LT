import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.forms import ModelForm,  widgets
from django.utils.translation import gettext_lazy as _

from logicaltasks.models import Comment


# class CommentModelForm(ModelForm):
#
#     class Meta:
#         model = Comment
#
#         fields = ('text',)
#         labels = {
#             'text': 'Оставить комментарий'
#         }
#         widgets = {
#             'text': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'floatingTextarea2',
#                 'style': 'height: 100px',
#             })
#         }


class CommentForm(forms.Form):
    text = forms.CharField(required=False,
                           widget=forms.Textarea(attrs={
                               'class': 'form-control',
                               'id': 'floatingTextarea2',
                               'style': 'height: 100px',
                           }),
                           label='Оставить комментарий')

    def clean_text(self):
        data = self.cleaned_data['text']
        # Check if a text doesn't content only spaces.
        if data is None or data.count(' ') == len(data):
            raise ValidationError(_('Недопустимый комментарий'))
        # Remember to always return the cleaned data.
        return data
