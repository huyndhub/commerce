from rest_framework import serializers
from apps.greeting.models import Greeting


class GreetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Greeting
        fields = [
            'id',
            'title',
        ]
