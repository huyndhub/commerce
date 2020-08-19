from rest_framework.generics import ListCreateAPIView

from apps.app_base.api.permission import TokenAuthentication

from ..models import Personal
from .serializers import PersonalSerializer


class ListCreateView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication, )
    queryset = Personal.objects.all()
    serializer_class = PersonalSerializer
