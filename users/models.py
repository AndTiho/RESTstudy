from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """Модель для пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите почту")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефонный номер", help_text="Введите номер телефона"
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Страна", help_text="Укажите страну проживания"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Payment(models.Model):
    """Модель для хранения данных о совершённых платежах

    Примечание:
    - Поле `course` может быть заполнено без `lesson` (оплата целого курса).
    - Поле `lesson` может быть заполнено без `course` (оплата отдельного урока).
    - Оба поля могут быть заполнены одновременно (курс + дополнительные уроки).
    """

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь платежа"
    )
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Оплаченный курс"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Оплаченный урок"
    )
    payment_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    payment_method = models.CharField(
        max_length=8, choices=PAYMENT_METHODS, default="transfer", verbose_name="Вид платежа"
    )

    def __str__(self):
        return f"{self.user} - {self.course}{self.lesson}. {self.payment_sum} рублей."

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"
        ordering = ["user"]
