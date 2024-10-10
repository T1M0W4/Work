from django.urls import path
from .views import HomePageView, SearchResultsView
from . import views

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('about/', views.about, name='about'),
]