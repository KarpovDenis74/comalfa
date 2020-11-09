from django import forms
from django.forms import ModelForm
from .models import Catalog


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Заполните, пожалуйста, это поле',
            params={'value': value},
        )
        

class SearchForm(forms.Form):
    name = forms.CharField(max_length=200, label="Введите наименование детали для поиска",
        validators=[validate_not_empty])

    class Meta:
        fields = ['name',]
        labels = {
            'name': 'Ищем по наименованию детали'
        }
        help_texts = {
            'name': 'Введите искомое название детали'
        }
