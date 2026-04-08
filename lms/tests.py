from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User

# Проверяем, что без у пользователя без авторизации нет на это прав
# Проверяем, что у пользователя "НЕ ВЛАДЕЛЬЦА" тоже нет на это прав
# Проверяем, что пользователь принадлежащий к группе модераторы так же не имеет на это прав
# Продолжаем тестирование, авторизуя пользователя


class LessonsAPITestCase(APITestCase):
    """Класс для тестирования нашей работы с уроками
    и подписки на курсы"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", is_active=True)
        self.user_not_owner = User.objects.create(email="test_not_owner@test.ru", is_active=True)
        self.user_is_moder = User.objects.create(email="test_is_moder@test.ru", is_active=True)
        moders_group, created = Group.objects.get_or_create(name="moders")
        self.user_is_moder.groups.add(moders_group)
        self.course = Course.objects.create(title="Test course", description="Test description", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson", description="Test description", course=self.course, owner=self.user
        )

    def tearDown(self):
        Lesson.objects.all().delete()

    def test_create_lesson(self):
        """Тестирование создания урока"""

        # Задаём основные данные для создания
        data = {
            "title": "Test Lesson",
            "description": "Test description",
        }

        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.post("/lesson/create/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что пользователь принадлежащий к группе модераторы тоже не имеет на это прав
        self.client.force_authenticate(user=self.user_is_moder)
        response = self.client.post("/lesson/create/", data=data, format="json")

        # Продолжаем тестирование, авторизуя пользователя
        self.client.force_authenticate(user=self.user)

        response = self.client.post("/lesson/create/", data=data, format="json")
        print(response.status_code)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(response.json()["title"], "Test Lesson")
        self.assertEqual(response.json()["description"], "Test description")
        self.assertEqual(response.json()["video_url"], None)
        self.assertEqual(response.json()["course"], None)
        self.assertEqual(response.json()["owner"], 1)
        self.assertTrue(Lesson.objects.filter(id=1).exists())

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""
        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.get("/lessons/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователь "НЕ ВЛАДЕЛЕЦ" тоже не видит не свои уроки
        self.client.force_authenticate(user=self.user_not_owner)
        response = self.client.get("/lessons/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"count": 0, "next": None, "previous": None, "results": []})

        # Проверяем, что пользователь модератор видит не свои уроки
        self.client.force_authenticate(user=self.user_is_moder)
        response = self.client.get("/lessons/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["title"], "Test Lesson")

        # Проверяем, что пользователь "ВЛАДЕЛЕЦ" так же видит свои уроки
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/lessons/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["title"], "Test Lesson")

    def test_view_lesson_detail(self):
        """Тестирование вывода деталей урока"""
        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.get(f"/lesson/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя "НЕ ВЛАДЕЛЬЦА" тоже нет на это прав
        self.client.force_authenticate(user=self.user_not_owner)
        response = self.client.get(f"/lesson/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Проверяем, что пользователь модератор видит детали урока не будучи "ВЛАДЕЛЬЦЕМ"
        self.client.force_authenticate(user=self.user_is_moder)
        response = self.client.get(f"/lesson/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["title"], "Test Lesson")
        self.assertEqual(data["description"], "Test description")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], self.course.pk)

        # Проверяем, что пользователь "ВЛАДЕЛЕЦ" так же видит свои уроки
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/lesson/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["title"], "Test Lesson")
        self.assertEqual(data["description"], "Test description")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], self.course.pk)

    def test_update_lesson(self):
        """Тестирование для изменения урока"""
        # Основные данные для теста
        data = {
            "title": "Test Lesson updated",
            "description": "Test description updated",
        }

        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.patch(f"/lesson/update/{self.lesson.pk}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя "НЕ ВЛАДЕЛЬЦА" тоже нет на это прав
        self.client.force_authenticate(user=self.user_not_owner)
        response = self.client.patch(f"/lesson/update/{self.lesson.pk}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Проверяем, что пользователь модератор имеет на это право
        self.client.force_authenticate(user=self.user_is_moder)
        response = self.client.patch(f"/lesson/update/{self.lesson.pk}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["title"], "Test Lesson updated")
        self.assertEqual(data["description"], "Test description updated")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], self.course.pk)

        # Проверяем, что пользователь "Владелец" тоже имеет на это право
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/lesson/update/{self.lesson.pk}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["title"], "Test Lesson updated")
        self.assertEqual(data["description"], "Test description updated")
        self.assertEqual(data["preview"], None)
        self.assertEqual(data["course"], self.course.pk)

    def test_delete_lesson(self):
        """Тестирование для удаления урока"""

        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.delete(f"/lesson/delete/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя "НЕ ВЛАДЕЛЬЦА" тоже нет на это прав
        self.client.force_authenticate(user=self.user_not_owner)
        response = self.client.delete(f"/lesson/delete/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Проверяем, что пользователь модератор так же не имеет на это право
        self.client.force_authenticate(user=self.user_is_moder)
        response = self.client.delete(f"/lesson/delete/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Проверяем, что только пользователь "Владелец" имеет на это право
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/lesson/delete/{self.lesson.pk}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_toggle_course_subscription(self):
        """Тестирование функционала подписки на курс"""

        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.post(f"/courses/{self.course.pk}/toggle-subscription/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Продолжаем тестирование с авторизированным пользователем
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/courses/{self.course.pk}/toggle-subscription/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Подписка добавлена")
        self.assertEqual(data["is_subscribed"], True)

        response = self.client.post(f"/courses/{self.course.pk}/toggle-subscription/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Подписка удалена")
        self.assertEqual(data["is_subscribed"], False)
