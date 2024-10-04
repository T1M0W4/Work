from django.urls import path
from . import views
from .views import UserProfileView, UserLoginView, RegisterView

app_name = 'auth'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
]