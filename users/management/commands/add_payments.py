from django.core.management.base import BaseCommand
from django.db import connection

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Add Users and their Payments (with links to Courses/Lessons)"

    def handle(self, *args, **options):

        User.objects.all().delete()
        Payment.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE users_payment_id_seq RESTART WITH 1;")

        # Создаём пользователей с корректным хэшированием пароля
        user_1, created = User.objects.get_or_create(email="moom200505@spam.ru", phone_number="+79151015846")
        if created or not user_1.has_usable_password():
            user_1.set_password("12345")  # ✅ Правильно: Django хэширует пароль
            user_1.is_active = True
            user_1.save()

        user_2, created = User.objects.get_or_create(email="moom200505@notspam.ru", phone_number="+79101015846")
        if created or not user_2.has_usable_password():
            user_2.set_password("54321")
            user_2.is_active = True
            user_2.save()

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
