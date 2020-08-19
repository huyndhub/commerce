from rest_framework import serializers

from apps.app_base.utils import decrypt

from ..models import Personal


class PersonalSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Personal
        fields = [
            'id',
            'full_name',
            'avatar',
            'gender',
            'date_of_birth',
            'address',
            'latitude',
            'longitude',
            'extra_info',
            'email',
        ]
        extra_kwargs = {
            'email': {'write_only': True},
            'extra_info': {'write_only': True},
        }

    def get_full_name(self, obj):
        return decrypt(obj.full_name) if obj.full_name else None
