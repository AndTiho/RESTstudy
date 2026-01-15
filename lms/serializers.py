from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация для модели Курсы"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для модели Уроки"""

    class Meta:
        model = Lesson
        fields = "__all__"
