from django.core.management.base import BaseCommand
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Add Courses and Lessons'

    def handle(self, *args, **options):
        course_1, _ = Course.objects.get_or_create(title='Python разработчик',
                                                description='Курс для начинающих Python разработчиков')
        course_2, _ = Course.objects.get_or_create(title='C++ разработчик',
                                                description='Курс для начинающих C++ разработчиков')

        lessons = [
            {'title': 'Начало Python', 'description': 'Знакомство с Python', 'course': course_1},
            {'title': 'Конец Python', 'description': 'Конец знакомства с Python', 'course': course_1},
            {'title': 'Начало C++', 'description': 'Знакомство с C++', 'course': course_2},
            {'title': 'Конец C++', 'description': 'Конец знакомства с C++', 'course': course_2}
        ]

        for lesson_data in lessons:
            lesson, created = Lesson.objects.get_or_create(**lesson_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added lesson: {lesson.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Lesson already exist: {lesson.title}'))
