import os

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_updated_email(subscriber_emails, course_title):
    """
    Функция, для отправки писем подписчикам курса.

    Принимает на вход:
    Список email пользователей
    Наименование курса
    """

    # Проверка на наличие почты для отправки
    if not subscriber_emails:
        return

    send_mail(
        subject=f"Курс '{course_title}' обновлён.",
        message="Курс,на который вы подписаны, обновился",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=subscriber_emails,
        fail_silently=True
    )