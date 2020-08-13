from django.urls import path
from apps.app_base.views import HomeView

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
]
