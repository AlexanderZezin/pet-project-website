from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя'
        }

    def clean_email(self):
        model = get_user_model()
        email = self.cleaned_data['email']
        if model.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким E-mail уже зарегестрирован')
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя или E-mail', widget=forms.TextInput())
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.CharField(disabled=True, label='E-mail')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())
