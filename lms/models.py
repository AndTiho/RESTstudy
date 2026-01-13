from django.db import models

class Course(models.Model):
    """Модель для учебного Курса"""
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описания")
    preview = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = 'курсы'
        ordering = ['title']

class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описания")
    preview = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Картинка')
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка")
    course= models.ForeignKey(Course, related_name='course', on_delete=models.PROTECT, verbose_name='Курс')

    def __str__(self):
        return f"{self.title}. Курс {self.course}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = 'уроки'
        ordering = ['title']
