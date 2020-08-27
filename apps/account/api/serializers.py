from rest_framework import serializers

from ..models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = [
            'id',
            'full_name',
            'avatar',
            'gender',
            'date_of_birth',
            'address',
            'extra_info',
        ]
        extra_kwargs = {
            'extra_info': {'write_only': True},
        }
