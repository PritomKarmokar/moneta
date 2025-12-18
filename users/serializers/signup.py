from rest_framework import serializers

from users.models import User
from applibs.helper import validate_email

class SignUpSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if not validate_email(email):
            raise serializers.ValidationError(detail='Invalid Email Address.', code='IEF_403')

        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise serializers.ValidationError(detail='An user with this email already exists.', code='UAE_403')
        return attrs