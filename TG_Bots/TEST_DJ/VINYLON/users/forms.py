from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=_('Подтвердите пароль'), widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': _('Имя пользователя'),
            'email': _('Электронная почта'),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(_('Пароли не совпадают'))
        return password_confirm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Имя пользователя'))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)
