from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson
from users.models import Payment, Price
from users.serializers import PaymentSerializer, PriceSerializer, UserPrivateSerializer, UserPublicSerializer

from .models import User
from .services import create_checkout_session, get_checkout_session_status


class UserCreateAPIView(CreateAPIView):
    """Регистрация нового пользователя"""

    serializer_class = UserPrivateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


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


class PriceCreateAPIView(CreateAPIView):
    """
    API для создания цены и ге4
    При создании объекта Price автоматически:
    - Сохраняет пользователя (request.user).
    - Создаёт сессию Stripe Checkout.
    - Обновляет поля session_id и checkout_url.
    """

    serializer_class = PriceSerializer
    queryset = Price.objects.all()

    def perform_create(self, serializer):

        # Получаем lesson_id из URL
        lesson_id = self.kwargs.get("lesson_id")
        course_id = self.kwargs.get("course_id")

        # Связываем с Lesson или Course
        if lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            serializer.save(user=self.request.user, lesson=lesson)
        elif course_id:
            course = get_object_or_404(Course, id=course_id)
            serializer.save(user=self.request.user, course=course)
        else:
            serializer.save(user=self.request.user)

        # 1. Сохраняем Price с текущим пользователем
        price = serializer.save(user=self.request.user)
        print("Price saved with ID:", price.id)  # ← Смотрите в терминале!

        try:
            session = create_checkout_session(price.stripe_price_id)
            price.session_id = session["session_id"]
            price.checkout_url = session["checkout_url"]
            price.save()
            print("Stripe session created:", session)  # ← Если не видно — ошибка здесь

            return Response(
                {
                    "id": price.id,
                    "session_id": price.session_id,
                    "checkout_url": price.checkout_url,
                    "message": "Сессия оплаты создана успешно.",
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            print("Stripe error:", str(e))  # ← Что именно упало?
            price.delete()
            return Response({"error": str(e)}, status=400)


class CheckoutSessionStatusView(APIView):
    """
    GET /api/stripe/session/{session_id}/status/
    Возвращает статус сессии Stripe Checkout.
    """

    def get(self, request, session_id):
        try:
            status_data = get_checkout_session_status(session_id)
            return Response(status_data, status=status.HTTP_200_OK)
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
