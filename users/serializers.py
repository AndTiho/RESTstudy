from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализация для модели платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserPrivateSerializer(serializers.ModelSerializer):
    """Сериализация для приватной модели пользователя"""

    payment_history = PaymentSerializer(source="payments", read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"


class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализация для публичной модели пользователя"""

    payment_history = PaymentSerializer(source="payments", read_only=True, many=True)

    class Meta:
        model = User
        fields = ["id", "is_active", "country", "avatar"]
