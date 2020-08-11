from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.greeting.models import Greeting
from .serializers import GreetingSerializer


class GreetingListCreateView(ListCreateAPIView):
    serializer_class = GreetingSerializer
    queryset = Greeting.objects.all()


class GreetingRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = GreetingSerializer
    queryset = Greeting.objects.all()
