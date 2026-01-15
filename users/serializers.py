from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация для модели пользователя"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "phone_number", "country", "avatar"]
