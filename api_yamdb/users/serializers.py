from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username cannot be "me"')
        return value


class TokenSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
