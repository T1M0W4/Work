from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
import logging
from .forms import UserRegistrationForm, UserLoginForm
from orders.models import Order

logger = logging.getLogger(__name__)

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(user=self.request.user)
        logger.debug(f"Загружены заказы для пользователя {self.request.user.username}")
        return context

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request, user)
        logger.info(f"Новый пользователь зарегистрирован: {user.username}")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Неудачная попытка регистрации. Ошибки: {form.errors}")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    
    def form_valid(self, form):
        logger.info(f"Пользователь {form.get_user().username} вошел в систему.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Неудачная попытка входа. Данные: {form.cleaned_data}")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("users:profile")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} вышел из системы.")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:profile")
    
    def form_valid(self, form):
        logger.info(f"Пользователь {self.request.user.username} изменил пароль.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Неудачная попытка смены пароля пользователем {self.request.user.username}. Ошибки: {form.errors}")
        return super().form_invalid(form)
