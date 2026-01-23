from rest_framework import serializers
from .models import Course, CourseSubscription, Lesson
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для модели Уроки"""

    video_url = serializers.URLField(validators=[UrlValidator("video_url")], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация для модели Курсы"""

    lesson_count = serializers.SerializerMethodField()
    all_lessons = LessonSerializer(source="lessons", read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    @staticmethod
    def get_lesson_count(obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Возвращает True, если текущий пользователь подписан на курс.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            return CourseSubscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"
