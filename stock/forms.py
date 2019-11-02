from django import forms


class DateInput(forms.DateInput):
    type = 'date'


class InputTest(forms.Form):
    date = forms.DateField(widget=DateInput)