import django_tables2 as tables
from .models import Speaker
from django import forms


class BallotForm(forms.Form):
    #title = forms.CharField()
    speaker_name = forms.ModelChoiceField(queryset=Speaker.objects.all(),
                                          to_field_name="name",
                                          widget=forms.Select(attrs={'style': 'width:200px' })
                                          )
    speaker_score = forms.IntegerField(widget=forms.NumberInput(attrs={'style':'width:100px'}))




