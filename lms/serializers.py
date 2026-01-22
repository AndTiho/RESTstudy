from rest_framework import serializers

from .models import Course, Lesson, CourseSubscription
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для модели Уроки"""

    video_url = serializers.URLField(validators=[UrlValidator('video_url')], required=False)

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
        user = self.context['request'].user
        if user.is_authenticated:
            return CourseSubscription.objects.filter(
                user=user,
                course=obj
            ).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"

# from rest_framework import serializers
# from .models import CourseSubscription
#
# class CourseSubscriptionSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(source='user.id')
#     course_id = serializers.IntegerField(source='course.id')
#     created_at = serializers.DateTimeField()
#
#     class Meta:
#         model = CourseSubscription
#         fields = ['user_id', 'course_id', 'created_at']
