from rest_framework import serializers

from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для модели Уроки"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация для модели Курсы"""
    lesson_count = serializers.SerializerMethodField()
    all_lessons = LessonSerializer(source='lessons', read_only=True, many=True)

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"


