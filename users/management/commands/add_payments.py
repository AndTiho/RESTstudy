from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Add Users and their Payments (with links to Courses/Lessons)"

    def handle(self, *args, **options):
        # Создаём пользователей
        user_1, _ = User.objects.get_or_create(
            email="moom200505@spam.ru", phone_number="+79151015846", password="12345"
        )
        user_2, _ = User.objects.get_or_create(
            email="moom200505@notspam.ru", phone_number="+79101015846", password="54321"
        )

        # Получаем существующие курсы и уроки из БД созданных кастомной командой add_materials
        try:
            course_python = Course.objects.get(title="Python разработчик")
            course_cpp = Course.objects.get(title="C++ разработчик")

            lesson_python_start = Lesson.objects.get(title="Начало Python", course=course_python)
            lesson_cpp_end = Lesson.objects.get(title="Конец C++", course=course_cpp)
        except Course.DoesNotExist:
            self.stderr.write("Ошибка: Курс не найден в БД!")
            return
        except Lesson.DoesNotExist:
            self.stderr.write("Ошибка: Урок не найден в БД!")
            return

        # Готовим данные для платежей (с реальными объектами)
        payments = [
            {"course": course_python, "payment_sum": 9999.99, "payment_method": "cash", "user": user_1},
            {"lesson": lesson_cpp_end, "payment_sum": 50.99, "payment_method": "transfer", "user": user_1},
            {"course": course_cpp, "payment_sum": 999, "payment_method": "cash", "user": user_2},
            {"lesson": lesson_python_start, "payment_sum": 100, "user": user_2},
        ]

        # Пытаемся создать платежи
        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added payment: {payment.user} for {payment.course or payment.lesson}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Payment already exists: {payment.user} for {payment.course or payment.lesson}"
                    )
                )
