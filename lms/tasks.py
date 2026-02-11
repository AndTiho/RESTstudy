import os

from django.core.mail import send_mail


def test():

    send_mail(
        subject="Обновление Курса",
        message="Курс,на который вы подписаны, обновился",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[user.email])