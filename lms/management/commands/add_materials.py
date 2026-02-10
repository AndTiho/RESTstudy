import stripe
from django.conf import settings
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.services import create_stripe_product_and_price

stripe.api_key = settings.STRIPE_API_KEY


class Command(BaseCommand):
    help = "Add Courses and Lessons with Stripe integration"

    def handle(self, *args, **options):

        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # Создаём курсы
        courses_data = [
            {
                "title": "Python разработчик",
                "description": "Курс для начинающих Python разработчиков",
                "price": 1000,
            },
            {
                "title": "C++ разработчик",
                "description": "Курс для начинающих C++ разработчиков",
                "price": 2000,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data["title"],
                defaults={
                    "description": course_data["description"],
                    "price": course_data["price"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added course: {course.title}"))
                # Создаём продукт и цену в Stripe для курса
                try:
                    product_id, price_id = create_stripe_product_and_price(course)
                    course.stripe_product_id = product_id
                    course.stripe_price_id = price_id
                    course.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Stripe IDs saved for course '{course.title}': " f"product={product_id}, price={price_id}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to create Stripe product/price for course '{course.title}': {e}")
                    )
            else:
                self.stdout.write(self.style.WARNING(f"Course already exists: {course.title}"))

        course_1 = Course.objects.get(title="Python разработчик")
        course_2 = Course.objects.get(title="C++ разработчик")

        lessons_data = [
            {
                "title": "Начало Python",
                "description": "Знакомство с Python",
                "course": course_1,
                "price": 200,
            },
            {
                "title": "Конец Python",
                "description": "Конец знакомства с Python",
                "course": course_1,
                "price": 200,
            },
            {
                "title": "Начало C++",
                "description": "Знакомство с C++",
                "course": course_2,
                "price": 200,
            },
            {
                "title": "Конец C++",
                "description": "Конец знакомства с C++",
                "course": course_2,
                "price": 200,
            },
        ]

        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                title=lesson_data["title"],
                course=lesson_data["course"],
                defaults={
                    "description": lesson_data["description"],
                    "price": lesson_data["price"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added lesson: {lesson.title}"))
                # Создаём продукт и цену в Stripe для урока
                try:
                    product_id, price_id = create_stripe_product_and_price(lesson)
                    lesson.stripe_product_id = product_id
                    lesson.stripe_price_id = price_id
                    lesson.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Stripe IDs saved for lesson '{lesson.title}': " f"product={product_id}, price={price_id}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to create Stripe product/price for lesson '{lesson.title}': {e}")
                    )
            else:
                self.stdout.write(self.style.WARNING(f"Lesson already exists: {lesson.title}"))
