import re
from django.core.exceptions import ValidationError

class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Получаем значение поля
        url = value.get(self.field)
        if url is None:
            return

        pattern = re.compile(
            r'^https?://(?:www\.)?youtube\.com/(?:watch\?v=|embed/|v/|shorts/|)[\w-]+'
        )

        if not pattern.match(url):
            raise ValidationError(
                f"Разрешены только ссылки на youtube.com. Получено: {url}"
            )
