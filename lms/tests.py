from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class LessonsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.ru',
            is_active=True  # Важно: иначе не сможет авторизоваться
        )
        self.user.set_password('12345')  # Хэшируем пароль
        self.user.save()


    def test_create_lesson(self):
        """Тестирование создания урока"""

        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Test Lesson",
            "description": "Test description",
        }
        response = self.client.post(
            "/lesson/create/",
            data=data,
            format='json'
        )

        print("Request URL:", response.request['PATH_INFO'])
        print("Status Code:", response.status_code)
        print("Response Content:", response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
