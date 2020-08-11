from django.urls import path
from .views import GreetingListCreateView, GreetingRetrieveUpdateDestroy


urlpatterns = [
    path('', GreetingListCreateView.as_view(), name='list-create-greeting'),
    path('<int:pk>', GreetingRetrieveUpdateDestroy.as_view(), name='retrieve-update-destroy-greeting'),
]
