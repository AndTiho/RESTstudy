from .models import Course
from .tasks import send_course_updated_email


def send_course_update_notification(course: Course, force: bool = False) -> None:
    """
    Отправляет уведомление подписчикам курса, если:
    - Прошло >4 часов с последнего обновления (по умолчанию).
    - Или `force=True` (отправить независимо от времени).

    Args:
        course: экземпляр Course
        force: принудительная отправка (без проверки времени)
    """
    if force:
        _send_notification(course)
        return

    if not course.was_updated_recently(hours=4):
        _send_notification(course)


def _send_notification(course: Course) -> None:
    """Внутренняя функция для отправки письма."""
    subscriber_emails = [
        sub.user.email
        for sub in course.subscribers.select_related('user').all()
    ]

    if subscriber_emails:
        send_course_updated_email.delay(
            subscriber_emails=subscriber_emails,
            course_title=course.title
        )
