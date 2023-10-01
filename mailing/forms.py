from django import forms
from django.forms import DateTimeInput

from mailing.models import Mailing, Client

# class StyleFormMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'


from django.forms import CheckboxInput, Select


class FormStyleMixin:
    fields: dict
    errors: dict

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, Select):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field_name in self.errors:
                form_classes: list[str] = field.widget.attrs['class'].split(' ')
                form_classes.append('is-invalid')
                field.widget.attrs['class'] = ' '.join(form_classes)


class MailingForm(FormStyleMixin, forms.ModelForm):

    start_time = forms.DateTimeField(
        label='Время начала',
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M')
    )

    end_time = forms.DateTimeField(
        label='Время окончания',
        required=False,
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M')
    )

    recipients = forms.ModelMultipleChoiceField(
        label='Получатели',
        required=False,
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Mailing
        fields = '__all__'
