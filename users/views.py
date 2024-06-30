from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from rest_framework import generics

from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from rest_framework_csv.renderers import CSVRenderer

from users.forms import RegisterUserForm, UserProfileForm, LoginUserForm, UserPasswordChangeForm
from users.mixins_csv import CSVFileMixin
from users.serializers import RegisterUserSerializer, ProfileUserSerializer, ChangePasswordSerializer


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация'
    }


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': 'Изменение пароля'}

    def get_success_url(self):
        return reverse_lazy('users:password_change_done')


class APIRegisterUser(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer


class APIProfileUser(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return self.request.user


class APIPasswordChangeUser(LoginRequiredMixin, generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class UserRender(CSVRenderer):
    header = ['username', 'email', 'first_name', 'last_name']


class APIUserCSV(CSVFileMixin, generics.RetrieveAPIView):
    renderer_classes = [UserRender]
    queryset = get_user_model().objects.all()
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return self.request.user

    def get_filename(self, request=None, *args, **kwargs):
        return f'{self.request.user.username}.csv'


class APIUserXLSX(XLSXFileMixin, generics.RetrieveAPIView):
    renderer_classes = [XLSXRenderer]
    queryset = get_user_model().objects.all()
    serializer_class = ProfileUserSerializer

    def get_object(self):
        return self.request.user

    def get_filename(self, request=None, *args, **kwargs):
        return f'{self.request.user.username}.xlsx'
