from django import forms
from .models import Grade, RATE_CHOICE

class GradeForm(forms.ModelForm):
    rate = forms.ChoiceField(choices=RATE_CHOICE, widget=forms.Select(), required=True)

    class Meta:
        model = Grade
        fields = ('content', 'rate')