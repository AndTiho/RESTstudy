from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsNotModerator, IsOwner, IsOwnerOrModerator


class CourseViewSet(ModelViewSet):
    """Для Курсов всё и сразу"""
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
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


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока (только для НЕ‑модераторов)."""

    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

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
    permission_classes = [IsOwnerOrModerator]

    def get_queryset(self):
        # Ограничиваем доступ для не‑модераторов
        if not self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Изменение урока:
    Владелец - свой урок;
    Модератор - любой урок.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrModerator]

    def get_queryset(self):
        if not self.request.user.groups.filter(name="moders").exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока (только владелец)."""

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()  # Модератор видит все уроки
        return Lesson.objects.filter(owner=user)  # Владелец — только свои
