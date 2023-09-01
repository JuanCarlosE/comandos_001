from django import forms

class RegisterForm(forms.Form):
    phone = forms.CharField(label="Telefono", max_length=15)