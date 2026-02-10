from django.conf import settings
from django.db import models


class Course(models.Model):
    """Модель для учебного Курса"""

    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описания")
    preview = models.ImageField(upload_to="photos/", null=True, blank=True, verbose_name="Картинка")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name="Стоимость курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания курса")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления курса")

    # поля для Страйпа
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID продукта Stripe")
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID цены Stripe")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]


class Lesson(models.Model):
    """Модель для уроков"""

    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описания")
    preview = models.ImageField(upload_to="photos/", null=True, blank=True, verbose_name="Картинка")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка")
    course = models.ForeignKey(
        Course, related_name="lessons", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Курс"
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name="Стоимость урока")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания урока")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления урока")

    # поля для Страйпа
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID продукта Stripe")
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID цены Stripe")

    def __str__(self):
        return f"{self.title} (курс: {self.course.title})"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]


class CourseSubscription(models.Model):
    """Модель сохраняющая данные о подписке пользователя на курс"""

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscribers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"
