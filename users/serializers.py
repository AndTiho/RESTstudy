from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализация для модели пользователя"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "phone_number", "country", "avatar"]


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация для модели платежей"""
    class Meta:
        model = Payment
        fields = '__all__'
