from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class RegistrationForm(forms.ModelForm):
    # Campos do modelo User que queremos no formulário
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(label='Email (será seu login)')
    
    # Campos extras que irão para o modelo Cliente ou para a senha
    celular = forms.CharField(max_length=15, label='Celular (com DDD)')
    data_nascimento = forms.DateField(label='Data de Nascimento', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não são iguais.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists(): # Verifica se o username (que será o email) já existe
            raise forms.ValidationError("Este email já está cadastrado no sistema.")
        return email

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if Cliente.objects.filter(celular=celular).exists():
            raise forms.ValidationError("Este número de celular já está cadastrado.")
        return celular

class ConvidadoForm(forms.Form):
    first_name = forms.CharField(max_length=150, label='Nome do Convidado')
    last_name = forms.CharField(max_length=150, label='Sobrenome do Convidado')
    email = forms.EmailField(label='Email do Convidado (será o login)')
    celular = forms.CharField(max_length=15, label='Celular do Convidado (com DDD)')
    data_nascimento = forms.DateField(label='Data de Nascimento do Convidado', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    password = forms.CharField(label='Criar Senha para o Convidado', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este email já está cadastrado no sistema.")
        return email

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if Cliente.objects.filter(celular=celular).exists():
            raise forms.ValidationError("Este número de celular já está cadastrado.")
        return celular