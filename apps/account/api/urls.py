from django.urls import path

from .views import ListCreateView, LoginView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name='account-login'),
    path('logout', LogoutView.as_view(), name='account-logout'),
    path('', ListCreateView.as_view(), name='account-list-create'),
]
