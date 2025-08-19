# Em agendamento/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    celular = forms.CharField(max_length=15, label='Celular (com DDD)')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não são iguais.')
        return cd['password2']

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if Cliente.objects.filter(celular=celular).exists():
            raise forms.ValidationError("Este número de celular já está cadastrado.")
        return celular