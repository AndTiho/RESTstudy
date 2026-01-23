from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonsAPITestCase(APITestCase):
    """Класс для тестирования нашей работы с уроками
    и подписки на курсы"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", is_active=True)
        self.user.set_password("12345")
        self.user.save()

    def tearDown(self):
        Lesson.objects.all().delete()

    def test_create_lesson(self):
        """Тестирование создания урока"""

        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Test Lesson",
            "description": "Test description",
        }
        response = self.client.post("/lesson/create/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "video_url": None,
                "title": "Test Lesson",
                "description": "Test description",
                "preview": None,
                "course": None,
                "owner": 1,
            },
        )
        self.assertTrue(Lesson.objects.filter(id=1).exists())

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""

        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(title="Test Lesson", description="Test description", owner=self.user)

        self.assertEqual(Lesson.objects.count(), 1)

        response = self.client.get("/lessons/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Теперь проверяем, что урок есть в ответе
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["title"], "Test Lesson")

    def test_view_lesson_detail(self):
        """Тестирование вывода деталей урока"""

        self.client.force_authenticate(user=self.user)

        lesson = Lesson.objects.create(title="Test Lesson", description="Test description", owner=self.user)

        self.assertEqual(Lesson.objects.count(), 1)

        response = self.client.get(f"/lesson/{lesson.pk}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["title"], "Test Lesson")
        self.assertEqual(data["description"], "Test description")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], None)

    def test_update_lesson(self):
        """Тестирование для изменения урока"""

        self.client.force_authenticate(user=self.user)

        lesson = Lesson.objects.create(title="Test Lesson", description="Test description", owner=self.user)

        data = {
            "title": "Test Lesson updated",
            "description": "Test description updated",
        }
        response = self.client.patch(f"/lesson/update/{lesson.pk}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["title"], "Test Lesson updated")
        self.assertEqual(data["description"], "Test description updated")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], None)

    def test_delete_lesson(self):
        """Тестирование для удаления урока"""

        self.client.force_authenticate(user=self.user)

        lesson = Lesson.objects.create(title="Test Lesson", description="Test description", owner=self.user)

        self.assertEqual(Lesson.objects.count(), 1)

        data = {
            "title": "Test Lesson updated",
            "description": "Test description updated",
        }

        response = self.client.delete(f"/lesson/delete/{lesson.pk}/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_toggle_course_subscription(self):
        """Тестирование функционала подписки на курс"""

        self.client.force_authenticate(user=self.user)

        course = Course.objects.create(title="Test course", description="Test description", owner=self.user)

        Lesson.objects.create(title="Test Lesson", description="Test description", course=course, owner=self.user)

        response = self.client.post(f"/courses/{course.id}/toggle-subscription/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Подписка добавлена")
        self.assertEqual(data["is_subscribed"], True)

        response = self.client.post(f"/courses/{course.id}/toggle-subscription/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Подписка удалена")
        self.assertEqual(data["is_subscribed"], False)
