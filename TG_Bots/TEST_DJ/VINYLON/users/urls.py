from django.urls import path
from .views import UserProfileView, UserLoginView, RegisterView, UserLogoutView, UserPasswordChangeView

app_name = 'auth'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserPasswordChangeView.as_view(), name='change_password'),
]
