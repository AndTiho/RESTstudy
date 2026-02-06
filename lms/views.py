from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, CourseSubscription, Lesson
from lms.paginators import MyPagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsNotModerator, IsOwner, IsOwnerOrModerator


class CourseViewSet(ModelViewSet):
    """Для Курсов всё и сразу"""

    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return Course.objects.none()

        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user.groups.filter(name="moders").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        permission_classes = []

        if self.action == "create":
            # Любой авторизованный, но НЕ модератор
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["update", "retrieve"]:
            # Владелец ИЛИ модератор
            permission_classes = [IsOwnerOrModerator]
        elif self.action == "destroy":
            # Только владелец (модераторы не могут удалять)
            permission_classes = [IsOwner]
        else:
            # Для list и других действий — базовая аутентификация
            permission_classes = [IsAuthenticated]

        # Возвращаем список экземпляров разрешений
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {"request": self.request}


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока (только для НЕ‑модераторов)."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Список уроков:
    - Владелец → только свои уроки.
    -Модератор → все уроки.
    """

    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр урока:
    -Владелец - свой урок.
    -Модератор - любой урок.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        return Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Изменение урока:
    Владелец - свой урок;
    Модератор - любой урок.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока (только владелец)."""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class ToggleCourseSubscriptionView(APIView):
    """
    POST /courses/<course_id>/toggle-subscription/
    Переключает подписку пользователя на курс:
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user

        course = get_object_or_404(Course, id=course_id)

        subscription = CourseSubscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
            is_subscribed = False
        else:
            CourseSubscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            is_subscribed = True

        return Response(
            {"message": message, "is_subscribed": is_subscribed, "course_id": course.id}, status=status.HTTP_200_OK
        )
