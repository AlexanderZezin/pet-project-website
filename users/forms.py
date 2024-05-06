from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username','first_name', 'email', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя'
        }

    def clean_email(self):
        model = get_user_model()
        cd = self.cleaned_data
        if model.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Пользователь с таким E-mail уже зарегестрирован')
        return self.cleaned_data['email']