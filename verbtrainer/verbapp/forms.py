from django import forms
from .models import IrregularVerb


class TrainerForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())
    base = forms.CharField(max_length=100)
    past_simple = forms.CharField(max_length=100)
    past_participle = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        editable_fields = kwargs.pop('editable_fields', [])
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if field_name not in editable_fields:
                self.fields[field_name].widget.attrs['readonly'] = True


class IrregularVerbForm(forms.ModelForm):
    class Meta:
        model = IrregularVerb
        fields = ['base', 'translation', 'past_simple', 'past_participle']