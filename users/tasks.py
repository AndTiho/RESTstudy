from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def check_login():
    """Проверка и блокировка пользователя по полю is_active
    если last_login был более 30 дней назад"""

    out_off_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=out_off_date, is_active=True)

    # Вариант для увеличения производительности, пусть будет тут
    # inactive_users.update(is_active=False)

    # Вариант для контроля кого деактивировали
    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Деактивирован пользователь: {user.email}")
