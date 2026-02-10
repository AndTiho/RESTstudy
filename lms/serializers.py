from rest_framework import serializers

from users.services import create_stripe_product_and_price

from .models import Course, CourseSubscription, Lesson
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация для модели Уроки"""

    def create(self, validated_data):
        # 1. Создаём объект (стандартный механизм DRF)
        lesson = super().create(validated_data)

        # 2. Синхронизируем с Stripe
        try:
            product_id, price_id = create_stripe_product_and_price(lesson)
            lesson.stripe_product_id = product_id
            lesson.stripe_price_id = price_id
            lesson.save(update_fields=["stripe_product_id", "stripe_price_id"])
        except Exception as e:
            # 3. Если ошибка Stripe — удаляем объект
            lesson.delete()
            raise serializers.ValidationError(f"Ошибка Stripe: {e}")

        return lesson

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализация для модели Курсы"""

    lesson_count = serializers.SerializerMethodField()
    all_lessons = LessonSerializer(source="lessons", read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    def create(self, validated_data):
        # Создаём объект Course
        course = Course.objects.create(**validated_data)

        # Синхронизируем с Stripe
        try:
            product_id, price_id = create_stripe_product_and_price(course)
            course.stripe_product_id = product_id
            course.stripe_price_id = price_id
            course.save()
        except Exception as e:
            # Если ошибка Stripe — удаляем курс или логируем
            course.delete()
            raise serializers.ValidationError(f"Ошибка Stripe: {e}")

        return course

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
