from rest_framework import serializers

from users.models import Payment, Price, User


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
        fields = ["id", "is_active", "country", "avatar", "payment_history"]


class PriceSerializer(serializers.ModelSerializer):

    stripe_price_id = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        model = Price
        fields = "__all__"
