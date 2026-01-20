from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment
from users.serializers import PaymentSerializer, UserPrivateSerializer, UserPublicSerializer

from .models import User


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserPrivateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(ListAPIView):
    """Список пользователей"""

    serializer_class = UserPublicSerializer
    queryset = User.objects.all()


class UserDetailView(RetrieveAPIView):
    """Просмотр профиля пользователя"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Возвращает разный сериализатор в зависимости от того,
        чей профиль просматривается.
        """
        user = self.get_object()
        if user == self.request.user or self.request.user.is_staff:
            # Свой профиль или админ — видим всё
            return UserPrivateSerializer
        else:
            # Чужой профиль — только публичная информация
            return UserPublicSerializer


class UserUpdateView(UpdateAPIView):
    """Обновление профиля только для себя"""

    serializer_class = UserPrivateSerializer
    queryset = User.objects.all()

    def get_object(self):
        # Разрешаем редактировать только свой профиль
        obj = super().get_object()
        if obj != self.request.user:
            self.permission_denied()
        return obj


class UserDeleteView(DestroyAPIView):
    """Удаление пользователя (только админ)"""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class PaymentListAPIView(generics.ListAPIView):
    """Контролер для списка платежей с применением фильтрации и сортировки"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
